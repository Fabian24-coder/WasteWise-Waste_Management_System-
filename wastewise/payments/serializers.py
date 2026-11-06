from rest_framework import serializers
from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            'id',
            'request',
            'amount',
            'payment_method',
            'payment_date',
            'payment_status',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError('Amount must be greater than zero.')
        return value

    def validate(self, data):
        pickup = data.get('request')
        payment_status = data.get('payment_status')

        # the pickup must be completed
        if pickup.request_status != 'completed':
            raise serializers.ValidationError('You can only pay for a completed pickup.')

        # the pickup must not already be paid
        if payment_status == 'completed':
            already_paid = Payment.objects.filter(request=pickup, payment_status='completed').exists()
            if already_paid:
                raise serializers.ValidationError('This pickup has already been paid.')

        return data