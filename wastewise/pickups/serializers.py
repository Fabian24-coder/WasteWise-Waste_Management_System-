from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import serializers

from rubbish.models import RubbishDetail
from .models import pickup_request

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "role"]


class WasteRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RubbishDetail
        fields = [
            "waste_id",
            "category",
            "name",
            "rate",
            "unit",
            "distance_rate_per_km",
            "description",
        ]


class PickUpRequestSerializer(serializers.ModelSerializer):
    user_detail = UserSerializer(source="user_id", read_only=True)
    collector_detail = UserSerializer(source="collector_id", read_only=True)
    waste_type_detail = WasteRateSerializer(source="waste_type", read_only=True)
    waste_type = serializers.PrimaryKeyRelatedField(
        queryset=RubbishDetail.objects.filter(is_active=True),
    )
    request_status = serializers.CharField(read_only=True)
    request_date = serializers.DateField(read_only=True)
    unit_rate = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    distance_rate_per_km = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True,
    )
    total_fee = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    payment_method = serializers.CharField(read_only=True)
    payment_status = serializers.CharField(read_only=True)
    scheduled_collection_at = serializers.DateTimeField(read_only=True)
    decline_reason = serializers.CharField(read_only=True)
    collector_message = serializers.CharField(read_only=True)
    paid_at = serializers.DateTimeField(read_only=True)
    collection_confirmed_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = pickup_request
        fields = [
            "id",
            "user_id",
            "user_detail",
            "collector_id",
            "collector_detail",
            "request_date",
            "request_status",
            "collection_date",
            "contact_name",
            "contact_number",
            "address",
            "waste_type",
            "waste_type_detail",
            "quantity",
            "distance_km",
            "unit_rate",
            "distance_rate_per_km",
            "total_fee",
            "payment_method",
            "payment_status",
            "scheduled_collection_at",
            "decline_reason",
            "collector_message",
            "paid_at",
            "collection_confirmed_at",
        ]
        read_only_fields = ["id", "user_id", "collector_id"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance is None:
            for name in ("contact_name", "contact_number", "address"):
                self.fields[name].required = True

    def validate_collection_date(self, value):
        if value < timezone.localdate():
            raise serializers.ValidationError("Choose today or a future collection date.")
        return value

    def create(self, validated_data):
        request = pickup_request(
            **validated_data,
            request_date=timezone.localdate(),
        )
        request.set_price_quote()
        request.save()
        return request

    def update(self, instance, validated_data):
        for field, value in validated_data.items():
            setattr(instance, field, value)
        instance.set_price_quote()
        instance.save()
        return instance
