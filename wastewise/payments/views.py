from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.permissions import IsAdminRole
from .models import Payment
from .serializers import PaymentSerializer



def is_admin(user):
    return user.role == 'admin' or user.is_superuser

def payments_for(user):
    # """The payments this user is allowed to see."""
    payments = Payment.objects.select_related('request').order_by('-payment_date')
    if is_admin(user):
        return payments
    if user.role == 'collector':
        return payments.filter(request__collector_id=user)
    return payments.filter(request__user_id=user)          # requestor


def can_pay_for(user, pickup):
    # """Is this user allowed to submit a payment for this pickup?"""
    if is_admin(user):
        return True
    if user.role == 'collector':
        return pickup.collector_id == user
    return pickup.user_id == user                           # requestor


@extend_schema(tags=['Payments'], responses=PaymentSerializer(many=True))
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def display_payments(request):
    payments = payments_for(request.user)
    serializer = PaymentSerializer(payments, many=True)
    return Response(serializer.data)


@extend_schema(tags=['Payments'], request=PaymentSerializer, responses=PaymentSerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def payment_create(request):
    serializer = PaymentSerializer(data=request.data)
    if serializer.is_valid():
        pickup = serializer.validated_data['request']
        if not can_pay_for(request.user, pickup):
            return Response({'detail': 'You can only pay for your own pickups.'},
                            status=status.HTTP_403_FORBIDDEN)
        serializer.save(amount=pickup.total_fee)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['Payments'], responses=PaymentSerializer)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def payment_get(request, pk):
    payment = get_object_or_404(payments_for(request.user), pk=pk)
    serializer = PaymentSerializer(payment)
    return Response(serializer.data)


@extend_schema(tags=['Payments'], responses={204: None})
@api_view(['DELETE'])
@permission_classes([IsAdminRole])
def payment_delete(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
    payment.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

# payment pages
@login_required
def payments_page(request):
    payments = payments_for(request.user).select_related('request__waste_type')
    page_obj = Paginator(payments, 10).get_page(request.GET.get("page"))
    context = {
        "payments": page_obj,
        "active_page": "payments",
    }
    return render(request, "payments/display_payments.html", context)