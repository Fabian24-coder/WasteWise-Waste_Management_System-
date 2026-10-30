from django import forms
from .models import pickup_request

class CreatePickupRequestForm(forms.ModelForm):
    class Meta:
        model = pickup_request
        fields = ['user_id', 'collector_id', 'request_date', 'request_status', 'collection_date']
        