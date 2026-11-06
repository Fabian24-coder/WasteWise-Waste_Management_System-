from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone

from .models import pickup_request


@transaction.atomic
def decide_request(
    pickup, collector, action, scheduled_collection_at=None,
    decline_reason="", collector_message="",
):
    pickup = pickup_request.objects.select_for_update().get(pk=pickup.pk)
    if pickup.request_status not in ("new", "pending"):
        raise ValidationError("Only new or pending requests can be actioned.")
    if pickup.collector_id and pickup.collector_id != collector.pk:
        raise ValidationError("This request is already assigned to another collector.")

    pickup.collector_id = collector
    pickup.collector_message = collector_message
    if action == "accept":
        if not scheduled_collection_at:
            raise ValidationError("A collection date and time are required to accept.")
        pickup.request_status = "accepted"
        pickup.scheduled_collection_at = scheduled_collection_at
        pickup.decline_reason = ""
    elif action == "decline":
        if not decline_reason.strip():
            raise ValidationError("A reason is required to decline the request.")
        pickup.request_status = "declined"
        pickup.scheduled_collection_at = None
        pickup.decline_reason = decline_reason.strip()
    else:
        raise ValidationError("Action must be accept or decline.")

    pickup.save(update_fields=[
        "collector_id",
        "collector_message",
        "request_status",
        "scheduled_collection_at",
        "decline_reason",
    ])
    return pickup


@transaction.atomic
def mark_payment_received(pickup):
    pickup = pickup_request.objects.select_for_update().get(pk=pickup.pk)
    if pickup.request_status != "accepted" or not pickup.scheduled_collection_at:
        raise ValidationError("Payment is available only for an accepted, scheduled request.")
    if timezone.localdate(pickup.scheduled_collection_at) != timezone.localdate():
        raise ValidationError("Cash payment can only be confirmed on the collection day.")
    if pickup.payment_status == "paid":
        raise ValidationError("Payment has already been confirmed.")

    pickup.payment_status = "paid"
    pickup.paid_at = timezone.now()
    pickup.save(update_fields=["payment_status", "paid_at"])
    return pickup


@transaction.atomic
def confirm_collection(pickup):
    pickup = pickup_request.objects.select_for_update().get(pk=pickup.pk)
    if pickup.request_status != "accepted" or not pickup.scheduled_collection_at:
        raise ValidationError("Only an accepted, scheduled request can be confirmed.")
    if timezone.localdate(pickup.scheduled_collection_at) != timezone.localdate():
        raise ValidationError("Collection can only be confirmed on the scheduled day.")
    if pickup.payment_status != "paid":
        raise ValidationError("Confirm the cash payment before confirming collection.")

    pickup.request_status = "collected"
    pickup.collection_confirmed_at = timezone.now()
    pickup.save(update_fields=["request_status", "collection_confirmed_at"])
    return pickup
