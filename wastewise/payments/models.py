from django.db import models
from django.utils import timezone

# Create your models here.

class Payment(models.Model):
    METHOD_OPTIONS = [
        ('cash', 'Cash'),
        ('mobile_money', 'Mobile Money'),
    ]

    STATUS_OPTIONS = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    request = models.ForeignKey('pickups.pickup_request', on_delete=models.PROTECT, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=METHOD_OPTIONS, default='cash')
    payment_date = models.DateTimeField(default=timezone.now)
    payment_status = models.CharField(max_length=20, choices=STATUS_OPTIONS, default='pending')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Payment {self.id}: {self.amount} ({self.get_payment_status_display()})"