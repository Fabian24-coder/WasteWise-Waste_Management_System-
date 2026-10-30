from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class pickup_request(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("completed", "Completed"),
    ]

    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    collector_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='collector')
    request_date = models.DateField(null=False, blank=False)
    request_status = models.CharField(max_length=100, null=False, blank=False, choices=STATUS_CHOICES)
    collection_date = models.DateField(null=False, blank=False)


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.request_date} {self.request_status} {self.collection_date}"