from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST
from rest_framework import serializers, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.permissions import IsAdminRole, IsCollector, IsRequestor
from rubbish.models import RubbishDetail
from .forms import CollectorDecisionForm, CreatePickUpRequestForm
from .models import pickup_request
from .serializers import PickUpRequestSerializer, WasteRateSerializer
from .services import confirm_collection, decide_request, mark_payment_received


def _request_role_allowed(user):
    return user.role in ("requestor", "collector", "admin") or user.is_superuser


@login_required
def pickup_dashboard(request):
    if not _request_role_allowed(request.user):
        return HttpResponseForbidden()
    pickup_requests = pickup_request.objects.select_related(
        "user_id", "collector_id", "waste_type",
    ).order_by("-id")
    if request.user.role == "requestor":
        pickup_requests = pickup_requests.filter(user_id=request.user)

    today = timezone.localdate()
    collection_day_requests = pickup_requests.none()
    if request.user.role == "requestor":
        collection_day_requests = pickup_requests.filter(
            request_status="accepted",
            scheduled_collection_at__date=today,
        ).order_by("scheduled_collection_at")

    return render(request, "pickups/dashboard.html", {
        "active_page": "dashboard",
        "requestor_role": request.user.role == "requestor",
        "total_requests": pickup_requests.count(),
        "pending_requests": pickup_requests.filter(
            request_status__in=("new", "pending"),
        ).count(),
        "collected_requests": pickup_requests.filter(
            request_status="collected",
        ).count(),
        "unpaid_requests": pickup_requests.filter(
            request_status="accepted",
            payment_status="unpaid",
        ).count(),
        "collector_count": get_user_model().objects.filter(role="collector").count(),
        "recent_requests": pickup_requests[:5],
        "collection_day_requests": collection_day_requests,
        "today": today,
        "waste_types": RubbishDetail.objects.filter(is_active=True).order_by(
            "category", "name",
        )[:5],
    })


@login_required
def pickup_request_views(request):
    if not _request_role_allowed(request.user):
        return HttpResponseForbidden()
    pickup_requests = pickup_request.objects.select_related(
        "user_id", "collector_id", "waste_type",
    ).order_by("-id")
    if request.user.role == "requestor":
        pickup_requests = pickup_requests.filter(user_id=request.user)
    page = Paginator(pickup_requests, 10).get_page(request.GET.get("page", 1))
    return render(request, "pickups/display_pickup_requests.html", {
        "page": page,
        "today": timezone.localdate(),
        "active_page": "requests",
    })


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def api_pickup_request_list(request):
    if not _request_role_allowed(request.user):
        return Response({"detail": "You do not have a supported account role."},
                        status=status.HTTP_403_FORBIDDEN)
    pickup_requests = pickup_request.objects.select_related(
        "user_id", "collector_id", "waste_type",
    ).order_by("-id")
    if request.user.role == "requestor":
        pickup_requests = pickup_requests.filter(user_id=request.user)
    serializer = PickUpRequestSerializer(pickup_requests, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def api_waste_rates(request):
    items = RubbishDetail.objects.filter(is_active=True).order_by("category", "name")
    return Response(WasteRateSerializer(items, many=True).data)


@login_required
def place_pickUp_request_Views(request):
    if request.user.role != "requestor":
        return HttpResponseForbidden()
    form = CreatePickUpRequestForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        pickup = form.save(commit=False)
        pickup.user_id = request.user
        pickup.request_date = timezone.localdate()
        pickup.request_status = "new"
        pickup.payment_method = "cash"
        pickup.set_price_quote()
        pickup.save()
        messages.success(request, "Collection request submitted with a calculated fee.")
        return redirect("pickups:display_pickup_requests")
    return render(request, "pickups/make_pickup_request.html", {
        "make_pickup_request": form,
        "waste_rates": RubbishDetail.objects.filter(is_active=True).order_by("category", "name"),
        "active_page": "create_request",
    })


@api_view(["POST"])
@permission_classes([IsRequestor])
def api_place_pickup_request(request):
    serializer = PickUpRequestSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user_id=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@login_required
def update_pickup_requests(request, pickup_request_id):
    if request.user.role != "collector":
        return HttpResponseForbidden()
    pickup = get_object_or_404(pickup_request, id=pickup_request_id)
    form = CollectorDecisionForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        try:
            decide_request(
                pickup=pickup,
                collector=request.user,
                **form.cleaned_data,
            )
        except ValidationError as error:
            form.add_error(None, error)
        else:
            messages.success(request, "The request status has been updated.")
            return redirect("pickups:display_pickup_requests")
    return render(request, "pickups/update_pickup_request.html", {
        "update_pickup_request": form,
        "pickup": pickup,
        "active_page": "requests",
    })


class CollectorDecisionSerializer(serializers.Serializer):
    action = serializers.ChoiceField(choices=("accept", "decline"))
    scheduled_collection_at = serializers.DateTimeField(required=False)
    decline_reason = serializers.CharField(required=False, allow_blank=True)
    collector_message = serializers.CharField(required=False, allow_blank=True)

    def validate(self, attrs):
        if attrs["action"] == "accept" and not attrs.get("scheduled_collection_at"):
            raise serializers.ValidationError({
                "scheduled_collection_at": "Set the collection date and time."
            })
        if (
            attrs.get("scheduled_collection_at")
            and attrs["scheduled_collection_at"] <= timezone.now()
        ):
            raise serializers.ValidationError({
                "scheduled_collection_at": "Choose a future collection time."
            })
        if attrs["action"] == "decline" and not attrs.get("decline_reason", "").strip():
            raise serializers.ValidationError({
                "decline_reason": "Give a reason for declining this request."
            })
        return attrs


@api_view(["POST"])
@permission_classes([IsCollector])
def api_decide_pickup_request(request, pickup_request_id):
    pickup = get_object_or_404(pickup_request, id=pickup_request_id)
    serializer = CollectorDecisionSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    try:
        pickup = decide_request(pickup, request.user, **serializer.validated_data)
    except ValidationError as error:
        return Response({"detail": error.messages}, status=status.HTTP_400_BAD_REQUEST)
    return Response(PickUpRequestSerializer(pickup).data)


@api_view(["POST"])
@permission_classes([IsRequestor])
def api_confirm_payment(request, pickup_request_id):
    pickup = get_object_or_404(pickup_request, id=pickup_request_id, user_id=request.user)
    try:
        pickup = mark_payment_received(pickup)
    except ValidationError as error:
        return Response({"detail": error.messages}, status=status.HTTP_400_BAD_REQUEST)
    return Response(PickUpRequestSerializer(pickup).data)


@api_view(["POST"])
@permission_classes([IsRequestor])
def api_confirm_collection(request, pickup_request_id):
    pickup = get_object_or_404(pickup_request, id=pickup_request_id, user_id=request.user)
    try:
        pickup = confirm_collection(pickup)
    except ValidationError as error:
        return Response({"detail": error.messages}, status=status.HTTP_400_BAD_REQUEST)
    return Response(PickUpRequestSerializer(pickup).data)


@login_required
@require_POST
def confirm_payment(request, pickup_request_id):
    if request.user.role != "requestor":
        return HttpResponseForbidden()
    pickup = get_object_or_404(
        pickup_request, id=pickup_request_id, user_id=request.user,
    )
    try:
        mark_payment_received(pickup)
    except ValidationError as error:
        messages.error(request, "; ".join(error.messages))
    else:
        messages.success(request, "Cash payment confirmed.")
    return redirect("pickups:display_pickup_requests")


@login_required
@require_POST
def confirm_pickup_collection(request, pickup_request_id):
    if request.user.role != "requestor":
        return HttpResponseForbidden()
    pickup = get_object_or_404(
        pickup_request, id=pickup_request_id, user_id=request.user,
    )
    try:
        confirm_collection(pickup)
    except ValidationError as error:
        messages.error(request, "; ".join(error.messages))
    else:
        messages.success(request, "Collection confirmed.")
    return redirect("pickups:display_pickup_requests")


@api_view(["PUT", "PATCH"])
@permission_classes([IsAuthenticated, IsAdminRole])
def api_update_pickup_request(request, pickup_request_id):
    pickup = get_object_or_404(pickup_request, id=pickup_request_id)
    serializer = PickUpRequestSerializer(
        pickup, data=request.data, partial=request.method == "PATCH",
    )
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@login_required
@require_POST
def delete_pickup_request(request, pickup_request_id):
    if request.user.role != "admin" and not request.user.is_superuser:
        return HttpResponseForbidden()
    get_object_or_404(pickup_request, id=pickup_request_id).delete()
    return redirect("pickups:display_pickup_requests")


@api_view(["DELETE"])
@permission_classes([IsAuthenticated, IsAdminRole])
def api_delete_pickup_request(request, pickup_request_id):
    get_object_or_404(pickup_request, id=pickup_request_id).delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
