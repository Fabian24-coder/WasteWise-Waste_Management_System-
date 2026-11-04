from rest_framework import serializers
from django.contrib.auth.models import User
from .models import pickup_request

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class PickUpRequestSerializer(serializers.ModelSerializer):
    # This is OptionalNested serializers to show user details instead of just IDs on GET requests
    user_detail = UserSerializer(source='user_id', read_only=True)
    collector_detail = UserSerializer(source='collector_id', read_only=True)

    class Meta:
        model = pickup_request
        fields = [
            'id', 
            'user_id', 'user_detail', 
            'collector_id', 'collector_detail', 
            'request_date', 
            'request_status', 
            'collection_date'
        ]
        extra_kwargs = {
            'user_id': {'write_only': True},
            'collector_id': {'write_only': True}
        }
