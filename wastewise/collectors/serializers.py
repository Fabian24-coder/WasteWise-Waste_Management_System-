from rest_framework import serializers
from .models import Zone, Collector


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