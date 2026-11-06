from django.shortcuts import get_object_or_404
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.permissions import IsAdminRole
from .models import Zone, Collector
from .serializers import ZoneSerializer, CollectorSerializer

# Create your views here.
# zone
@extend_schema(
    tags=["Zones"],
    summary="List zones",
    responses={200: ZoneSerializer(many=True), 401: OpenApiResponse(description="Authentication required")},
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def display_zones(request):
    zones = Zone.objects.all()
    serializer = ZoneSerializer(zones, many=True)
    return Response(serializer.data)


@extend_schema(
    tags=["Zones"],
    summary="Create a zone",
    request=ZoneSerializer,
    responses={
        201: ZoneSerializer,
        400: OpenApiResponse(description="Invalid zone details"),
        403: OpenApiResponse(description="Admin role required"),
    },
)
@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminRole])
def zone_create(request):
    serializer = ZoneSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    tags=["Zones"],
    summary="Get a zone",
    responses={
        200: ZoneSerializer,
        401: OpenApiResponse(description="Authentication required"),
        404: OpenApiResponse(description="Zone not found"),
    },
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def zone_get(request, pk):
    zone = get_object_or_404(Zone, pk=pk)
    serializer = ZoneSerializer(zone)
    return Response(serializer.data)

@extend_schema(
    tags=["Zones"],
    summary="Update a zone",
    request=ZoneSerializer,
    responses={
        200: ZoneSerializer,
        400: OpenApiResponse(description="Invalid zone details"),
        403: OpenApiResponse(description="Admin role required"),
        404: OpenApiResponse(description="Zone not found"),
    },
)
@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated, IsAdminRole])
def zone_update(request, pk):
    zone = get_object_or_404(Zone, pk=pk)
    serializer = ZoneSerializer(zone, data=request.data, partial=(request.method == 'PATCH'))
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    tags=["Zones"],
    summary="Delete a zone",
    responses={
        204: OpenApiResponse(description="Zone deleted"),
        403: OpenApiResponse(description="Admin role required"),
        404: OpenApiResponse(description="Zone not found"),
    },
)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsAdminRole])
def zone_delete(request, pk):
    zone = get_object_or_404(Zone, pk=pk)
    zone.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


# Collectors

@extend_schema(
    tags=["Collectors"],
    summary="List collector profiles",
    responses={
        200: CollectorSerializer(many=True),
        401: OpenApiResponse(description="Authentication required"),
    },
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def display_collectors(request):
    collectors = Collector.objects.select_related('user', 'zone')
    serializer = CollectorSerializer(collectors, many=True)
    return Response(serializer.data)


@extend_schema(
    tags=["Collectors"],
    summary="Create a collector profile",
    description="Admin-only. The user must already have the collector role.",
    request=CollectorSerializer,
    responses={
        201: CollectorSerializer,
        400: OpenApiResponse(description="Invalid collector profile"),
        403: OpenApiResponse(description="Admin role required"),
    },
)
@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminRole])
def collector_create(request):
    serializer = CollectorSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    tags=["Collectors"],
    summary="Get a collector profile",
    responses={
        200: CollectorSerializer,
        401: OpenApiResponse(description="Authentication required"),
        404: OpenApiResponse(description="Collector not found"),
    },
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def collector_get(request, pk):
    collector = get_object_or_404(Collector, pk=pk)
    serializer = CollectorSerializer(collector)
    return Response(serializer.data)


@extend_schema(
    tags=["Collectors"],
    summary="Update a collector profile",
    request=CollectorSerializer,
    responses={
        200: CollectorSerializer,
        400: OpenApiResponse(description="Invalid collector profile"),
        403: OpenApiResponse(description="Admin role required"),
        404: OpenApiResponse(description="Collector not found"),
    },
)
@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated, IsAdminRole])
def collector_update(request, pk):
    collector = get_object_or_404(Collector, pk=pk)
    serializer = CollectorSerializer(collector, data=request.data, partial=(request.method == 'PATCH'))
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    tags=["Collectors"],
    summary="Delete a collector profile",
    responses={
        204: OpenApiResponse(description="Collector profile deleted"),
        403: OpenApiResponse(description="Admin role required"),
        404: OpenApiResponse(description="Collector not found"),
    },
)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsAdminRole])
def collector_delete(request, pk):
    collector = get_object_or_404(Collector, pk=pk)
    collector.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)