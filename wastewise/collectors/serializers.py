from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Zone, Collector

User = get_user_model()


class ZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zone
        fields = [
            'id', 
            'name', 
            'description'
        ]


class CollectorSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='user.get_full_name', read_only=True)
    zone_name = serializers.CharField(source='zone.name', read_only=True, default=None)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Collector
        fields = [
            'id',
            'user',
            'full_name',
            'phone_number',
            'zone',
            'zone_name',
            'status',
            'status_display',
            'is_available',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']

    def validate_user(self, user):
        if user.role != "collector":
            raise serializers.ValidationError(
                "The selected account must have the collector role."
            )
        return user