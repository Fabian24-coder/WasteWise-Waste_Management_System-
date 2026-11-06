from django import forms
from django.utils import timezone

from rubbish.models import RubbishDetail
from .models import pickup_request


class CreatePickUpRequestForm(forms.ModelForm):
    class Meta:
        model = pickup_request
        fields = [
            "contact_name",
            "contact_number",
            "address",
            "collection_date",
            "waste_type",
            "quantity",
            "distance_km",
        ]
        widgets = {
            "collection_date": forms.DateInput(attrs={"type": "date"}),
            "address": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["waste_type"].queryset = RubbishDetail.objects.filter(is_active=True)

    def clean_collection_date(self):
        collection_date = self.cleaned_data["collection_date"]
        if collection_date < timezone.localdate():
            raise forms.ValidationError("Choose today or a future collection date.")
        return collection_date


class CollectorDecisionForm(forms.Form):
    ACTION_CHOICES = [
        ("accept", "Accept request"),
        ("decline", "Decline request"),
    ]

    action = forms.ChoiceField(choices=ACTION_CHOICES)
    scheduled_collection_at = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"}),
    )
    decline_reason = forms.CharField(required=False, widget=forms.Textarea(attrs={"rows": 3}))
    collector_message = forms.CharField(required=False, widget=forms.Textarea(attrs={"rows": 3}))

    def clean(self):
        cleaned_data = super().clean()
        scheduled_at = cleaned_data.get("scheduled_collection_at")
        if scheduled_at and scheduled_at <= timezone.now():
            self.add_error("scheduled_collection_at", "Choose a future collection time.")
        if cleaned_data.get("action") == "accept" and not cleaned_data.get("scheduled_collection_at"):
            self.add_error("scheduled_collection_at", "Set the collection date and time.")
        if cleaned_data.get("action") == "decline" and not cleaned_data.get("decline_reason"):
            self.add_error("decline_reason", "Give a reason for declining this request.")
        return cleaned_data
