from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Zone, Collector
from .serializers import ZoneSerializer, CollectorSerializer

# Create your views here.
# zone
@extend_schema(responses=ZoneSerializer(many=True))
@api_view(['GET'])
def display_zones(request):
    zones = Zone.objects.all()
    serializer = ZoneSerializer(zones, many=True)
    return Response(serializer.data)


@extend_schema(request=ZoneSerializer, responses=ZoneSerializer)
@api_view(['POST'])
def zone_create(request):
    serializer = ZoneSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(responses=ZoneSerializer)
@api_view(['GET'])
def zone_get(request, pk):
    zone = get_object_or_404(Zone, pk=pk)
    serializer = ZoneSerializer(zone)
    return Response(serializer.data)

@extend_schema(request=ZoneSerializer, responses=ZoneSerializer)
@api_view(['PUT', 'PATCH'])
def zone_update(request, pk):
    zone = get_object_or_404(Zone, pk=pk)
    serializer = ZoneSerializer(zone, data=request.data, partial=(request.method == 'PATCH'))
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(responses={204: None})
@api_view(['DELETE'])
def zone_delete(request, pk):
    zone = get_object_or_404(Zone, pk=pk)
    zone.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


# Collectors

@extend_schema(responses=CollectorSerializer(many=True))
@api_view(['GET'])
def display_collectors(request):
    collectors = Collector.objects.select_related('user', 'zone')
    serializer = CollectorSerializer(collectors, many=True)
    return Response(serializer.data)


@extend_schema(request=CollectorSerializer, responses=CollectorSerializer)
@api_view(['POST'])
def collector_create(request):
    serializer = CollectorSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(responses=CollectorSerializer)
@api_view(['GET'])
def collector_get(request, pk):
    collector = get_object_or_404(Collector, pk=pk)
    serializer = CollectorSerializer(collector)
    return Response(serializer.data)


@extend_schema(request=CollectorSerializer, responses=CollectorSerializer)
@api_view(['PUT', 'PATCH'])
def collector_update(request, pk):
    collector = get_object_or_404(Collector, pk=pk)
    serializer = CollectorSerializer(collector, data=request.data, partial=(request.method == 'PATCH'))
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(responses={204: None})
@api_view(['DELETE'])
def collector_delete(request, pk):
    collector = get_object_or_404(Collector, pk=pk)
    collector.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)