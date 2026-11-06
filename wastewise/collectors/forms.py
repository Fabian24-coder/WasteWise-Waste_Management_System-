from django import forms
from .models import Zone, Collector
from django.contrib.auth import get_user_model

User = get_user_model()

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['user'].queryset = User.objects.filter(
            role='collector',
            collector_profile__isnull=True,
        )


class UpdateCollectorForm(forms.ModelForm):
    class Meta:
        model = Collector
        fields = ['phone_number', 'zone', 'status', 'is_available']