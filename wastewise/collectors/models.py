from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Zone(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)


    def __str__(self):
        return self.name

class Collector(models.Model):
    STATUS_OPTIONS = [
        ('pending', 'Pending'),
        ('active', 'Active'),
        ('suspended', 'Suspended')
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='collector_profile')
    phone_number = models.CharField(max_length=20)
    zone = models.ForeignKey(Zone, on_delete=models.SET_NULL, null=True, blank=True, related_name='collectors')
    status = models.CharField(max_length=20, choices=STATUS_OPTIONS, default='pending')
    is_available = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username
    