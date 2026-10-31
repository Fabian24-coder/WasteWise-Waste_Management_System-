from django import forms
from .models import pickup_request

class DisplayPickupRequestForm(forms.ModelForm):
    class Meta:
        model = pickup_request
        fields = ['user_id', 'collector_id', 'request_date', 'request_status', 'collection_date']


class CreatePickUpRequestForm(forms.ModelForm):
    class Meta:
        model = pickup_request
        fields = ['user_id', 'collector_id', 'request_date', 'request_status', 'collection_date']


class Update_pickup_requestForm(forms.ModelForm):
    class Meta:
        model = pickup_request
        fields = ['user_id', 'collector_id', 'request_date', 'request_status', 'collection_date']
       