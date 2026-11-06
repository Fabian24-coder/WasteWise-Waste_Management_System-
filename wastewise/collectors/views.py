from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_POST
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import IsAdminRole
from rest_framework.response import Response
from rest_framework import status

from .models import Zone, Collector
from .serializers import ZoneSerializer, CollectorSerializer
from .forms import CreateZoneForm, UpdateZoneForm, CreateCollectorForm, UpdateCollectorForm

# Create your views here.
# zone apis 
def is_admin(user):
    return user.is_authenticated and (user.role == 'admin' or user.is_superuser)
admin_required = user_passes_test(is_admin)

@extend_schema(tags=['Zones'],responses=ZoneSerializer(many=True))
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_display_zones(request):
    zones = Zone.objects.all()
    serializer = ZoneSerializer(zones, many=True)
    return Response(serializer.data)


@extend_schema(tags=['Zones'],request=ZoneSerializer, responses=ZoneSerializer)
@api_view(['POST'])
@permission_classes([IsAdminRole])
def api_zone_create(request):
    serializer = ZoneSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['Zones'],responses=ZoneSerializer)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_zone_get(request, pk):
    zone = get_object_or_404(Zone, pk=pk)
    serializer = ZoneSerializer(zone)
    return Response(serializer.data)

@extend_schema(tags=['Zones'],request=ZoneSerializer, responses=ZoneSerializer)
@api_view(['PUT', 'PATCH'])
@permission_classes([IsAdminRole])
def api_zone_update(request, pk):
    zone = get_object_or_404(Zone, pk=pk)
    serializer = ZoneSerializer(zone, data=request.data, partial=(request.method == 'PATCH'))
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(tags=['Zones'],responses={204: None})
@api_view(['DELETE'])
@permission_classes([IsAdminRole])
def api_zone_delete(request, pk):
    zone = get_object_or_404(Zone, pk=pk)
    zone.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


# Collector apis
@extend_schema(tags=["Collectors"], responses=CollectorSerializer(many=True))
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_display_collectors(request):
    collectors = Collector.objects.select_related('user', 'zone')
    serializer = CollectorSerializer(collectors, many=True)
    return Response(serializer.data)


@extend_schema(tags=["Collectors"],request=CollectorSerializer, responses=CollectorSerializer)
@api_view(['POST'])
@permission_classes([IsAdminRole])
def api_collector_create(request):
    serializer = CollectorSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=["Collectors"],responses=CollectorSerializer)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_collector_get(request, pk):
    collector = get_object_or_404(Collector, pk=pk)
    serializer = CollectorSerializer(collector)
    return Response(serializer.data)


@extend_schema(tags=["Collectors"],request=CollectorSerializer, responses=CollectorSerializer)
@api_view(['PUT', 'PATCH'])
@permission_classes([IsAdminRole])
def api_collector_update(request, pk):
    collector = get_object_or_404(Collector, pk=pk)
    serializer = CollectorSerializer(collector, data=request.data, partial=(request.method == 'PATCH'))
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=["Collectors"], responses={204: None})
@api_view(['DELETE'])
@permission_classes([IsAdminRole])
def api_collector_delete(request, pk):
    collector = get_object_or_404(Collector, pk=pk)
    collector.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


# zone pages
@admin_required
def display_zones(request):
    all_zones = Zone.objects.all().order_by("name")
    paginator = Paginator(all_zones, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    if request.method == "POST":
        zone_form = CreateZoneForm(request.POST)
        if zone_form.is_valid():
            zone_form.save()
            return redirect("collectors:display_zones")
    else:
        zone_form = CreateZoneForm()
    context = {
        "display_zones": page_obj,
        "create_zone": zone_form,
        "active_page": "zones"
    }
    return render(request, "collectors/display_zones.html", context)


@admin_required
def update_zone(request, zone_id):
    get_zone = get_object_or_404(Zone, id=zone_id)
    if request.method == "POST":
        update_zone_form = UpdateZoneForm(request.POST, instance=get_zone)
        if update_zone_form.is_valid():
            update_zone_form.save()
            return redirect("collectors:display_zones")
    else:
        update_zone_form = UpdateZoneForm(instance=get_zone)
    context = {
        "update_zone": update_zone_form,
        "active_page": "zones"
    }
    return render(request, "collectors/update_zone.html", context)


@admin_required
@require_POST
def delete_zone(request, zone_id):
    zone = get_object_or_404(Zone, id=zone_id)
    zone.delete()
    return redirect("collectors:display_zones")


# collector pages
@admin_required
def display_collectors(request):
    all_collectors = Collector.objects.all().order_by("-id").select_related("user", "zone")
    paginator = Paginator(all_collectors, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    if request.method == "POST":
        collector_form = CreateCollectorForm(request.POST)
        if collector_form.is_valid():
            collector_form.save()
            return redirect("collectors:display_collectors")
    else:
        collector_form = CreateCollectorForm()
    context = {
        "display_collectors": page_obj,
        "create_collector": collector_form,
        "active_page": "collectors"
    }
    return render(request, "collectors/display_collectors.html", context)


@admin_required
def update_collector(request, collector_id):
    get_collector = get_object_or_404(Collector, id=collector_id)
    if request.method == "POST":
        update_collector_form = UpdateCollectorForm(request.POST, instance=get_collector)
        if update_collector_form.is_valid():
            update_collector_form.save()
            return redirect("collectors:display_collectors")
    else:
        update_collector_form = UpdateCollectorForm(instance=get_collector)
    context = {
        "update_collector": update_collector_form,
        "active_page": "collectors"
    }
    return render(request, "collectors/update_collector.html", context)


@admin_required
@require_POST
def delete_collector(request, collector_id):
    collector = get_object_or_404(Collector, id=collector_id)
    collector.delete()
    return redirect("collectors:display_collectors")