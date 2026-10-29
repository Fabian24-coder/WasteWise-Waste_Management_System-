from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class pickup_request(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    collector_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='collector')
    request_date = models.DateField(null=False, blank=False)
    request_status = models.CharField(max_length=100, null=False, blank=False)
    collection_date = models.DateField(null=False, blank=False)
    
    def __str__(self):
        return f"{self.request_date} {self.request_status} {self.collection_date}"