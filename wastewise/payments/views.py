from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from .models import Payment
from .serializers import PaymentSerializer

# Create your views here.

@extend_schema(responses=PaymentSerializer(many=True))
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def display_payments(request):
    payments = Payment.objects.select_related('request').order_by('-payment_date')
    serializer = PaymentSerializer(payments, many=True)
    return Response(serializer.data)


@extend_schema(request=PaymentSerializer, responses=PaymentSerializer)
@api_view(['POST'])
@permission_classes([IsAdminUser])
def payment_create(request):
    serializer = PaymentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(responses=PaymentSerializer)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def payment_get(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
    serializer = PaymentSerializer(payment)
    return Response(serializer.data)


@extend_schema(request=PaymentSerializer, responses=PaymentSerializer)
@api_view(['PUT', 'PATCH'])
@permission_classes([IsAdminUser])
def payment_update(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
    serializer = PaymentSerializer(payment, data=request.data, partial=(request.method == 'PATCH'))
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(responses={204: None})
@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def payment_delete(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
    payment.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)