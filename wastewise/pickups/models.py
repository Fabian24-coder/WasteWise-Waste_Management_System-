from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from django.conf import settings

from rubbish.models import RubbishDetail

# Create your models here.

class pickup_request(models.Model):
    STATUS_CHOICES = [
        ("new", "New request"),
        ("pending", "Pending"),
        ("accepted", "Accepted"),
        ("declined", "Declined"),
        ("collected", "Collected"),
    ]
    PAYMENT_STATUS_CHOICES = [
        ("unpaid", "Unpaid"),
        ("paid", "Paid"),
    ]

    user_id = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name="pickup_requests",
    )
    collector_id = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="assigned_pickup_requests",
    )
    request_date = models.DateField(null=False, blank=False)
    request_status = models.CharField(
        max_length=100, null=False, blank=False, choices=STATUS_CHOICES, default="new",
    )
    collection_date = models.DateField(null=False, blank=False)
    contact_name = models.CharField(max_length=150, blank=True)
    contact_number = models.CharField(max_length=30, blank=True)
    address = models.TextField(blank=True)
    waste_type = models.ForeignKey(
        RubbishDetail, on_delete=models.PROTECT, null=True, blank=True,
        related_name="pickup_requests",
    )
    quantity = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal("1"),
        validators=[MinValueValidator(Decimal("0.01"))],
    )
    distance_km = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal("0"),
        validators=[MinValueValidator(Decimal("0"))],
    )
    unit_rate = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0"))
    distance_rate_per_km = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal("0"),
    )
    total_fee = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0"))
    scheduled_collection_at = models.DateTimeField(null=True, blank=True)
    decline_reason = models.TextField(blank=True)
    collector_message = models.TextField(blank=True)
    payment_method = models.CharField(max_length=20, default="cash")
    payment_status = models.CharField(
        max_length=20, choices=PAYMENT_STATUS_CHOICES, default="unpaid",
    )
    paid_at = models.DateTimeField(null=True, blank=True)
    collection_confirmed_at = models.DateTimeField(null=True, blank=True)

    def calculate_total_fee(self):
        return (
            self.quantity * self.unit_rate
            + self.distance_km * self.distance_rate_per_km
        ).quantize(Decimal("0.01"))

    def set_price_quote(self):
        if self.waste_type_id:
            self.unit_rate = self.waste_type.rate
            self.distance_rate_per_km = self.waste_type.distance_rate_per_km
        self.total_fee = self.calculate_total_fee()

    def __str__(self):
        return f"{self.request_date} {self.request_status} {self.collection_date}"
