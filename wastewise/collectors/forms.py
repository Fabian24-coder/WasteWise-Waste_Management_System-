from django import forms
from .models import Zone, Collector


class CreateZoneForm(forms.ModelForm):
    class Meta:
        model = Zone
        fields = ['name', 'description']


class UpdateZoneForm(forms.ModelForm):
    class Meta:
        model = Zone
        fields = ['name', 'description']


class CreateCollectorForm(forms.ModelForm):
    class Meta:
        model = Collector
        fields = ['user', 'phone_number', 'zone', 'status', 'is_available']


class UpdateCollectorForm(forms.ModelForm):
    class Meta:
        model = Collector
        fields = ['phone_number', 'zone', 'status', 'is_available']