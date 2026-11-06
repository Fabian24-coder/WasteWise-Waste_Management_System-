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
            'transaction_reference',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['amount', 'payment_status', 'created_at', 'updated_at']

    def validate(self, data):
        # the saved payment when updating, None when creating
        payment = self.instance

        if payment is None:
            pickup = data.get('request')
            method = data.get('payment_method', 'cash')
            reference = data.get('transaction_reference', '')
        else:
            # updating: use what was sent, otherwise keep the saved value
            pickup = data.get('request', payment.request)
            method = data.get('payment_method', payment.payment_method)
            reference = data.get('transaction_reference', payment.transaction_reference)

        #  for a new payment
        if payment is None:
            # if collector accepted the pickup
            if pickup.request_status != 'accepted':
                raise serializers.ValidationError('Payment can only be made for an accepted pickup.')

            # the pickup must not already be paid
            if pickup.payment_status == 'paid':
                raise serializers.ValidationError('This pickup has already been paid.')

            # payment waiting for confirmation at a time
            waiting = Payment.objects.filter(request=pickup, payment_status='pending')
            if waiting.exists():
                raise serializers.ValidationError('This pickup already has a payment waiting for confirmation.')

        # all payments, mobile money must have a reference code
        if method == 'mobile_money' and reference.strip() == '':
            raise serializers.ValidationError(
                {'transaction_reference': 'A transaction reference is required for mobile money.'}
            )

        return data