from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from pickups.models import pickup_request
from .models import Payment


@receiver(post_save, sender=pickup_request)
def record_payment(sender, instance, **kwargs):
    pickup = instance

    # Only act when the pickup is paid
    if pickup.payment_status != 'paid':
        return

    # Already has a completed payment Nothing to do
    if pickup.payments.filter(payment_status='completed').exists():
        return

    paid_time = pickup.paid_at or timezone.now()

    # A payment is waiting e.g mobile money reference)? Complete it
    waiting = pickup.payments.filter(payment_status='pending').first()
    if waiting:
        waiting.payment_status = 'completed'
        waiting.payment_date = paid_time
        waiting.save()
        return

    # Nothing was submitted, so it was cash: create the receipt
    Payment.objects.create(
        request=pickup,
        amount=pickup.total_fee,
        payment_method='cash',
        payment_status='completed',
        payment_date=paid_time,
    )