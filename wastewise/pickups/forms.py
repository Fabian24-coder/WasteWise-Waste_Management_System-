from django import forms
from .models import pickup_request

calendar_widget = {
    'request_date': forms.DateInput(
        attrs={'type': 'date', 'class': 'form-control'}
    ),
    'collection_date': forms.DateInput(
        attrs={'type': 'date', 'class': 'form-control'}
    ),
}

class DisplayPickupRequestForm(forms.ModelForm):
    class Meta:
        model = pickup_request
        fields = ['user_id', 'collector_id', 'request_date', 'request_status', 'collection_date']
        widgets = calendar_widget

class CreatePickUpRequestForm(forms.ModelForm):
    class Meta:
        model = pickup_request
        fields = ['user_id', 'collector_id', 'request_date', 'request_status', 'collection_date']
        widgets = calendar_widget


class Update_pickup_requestForm(forms.ModelForm):
    class Meta:
        model = pickup_request
        fields = ['user_id', 'collector_id', 'request_date', 'request_status', 'collection_date']
        widgets = calendar_widget
