from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from django.db import transaction

from profiles.models import Profile

from .models import User


PROFILE_FIELDS = ("phone_number", "address", "street", "city")


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    phone_number = serializers.CharField(max_length=20, required=False, allow_blank=True, write_only=True)
    address = serializers.CharField(max_length=255, required=False, allow_blank=True, write_only=True)
    street = serializers.CharField(max_length=255, required=False, allow_blank=True, write_only=True)
    city = serializers.CharField(max_length=100, required=False, allow_blank=True, write_only=True)

    class Meta:
        model = User
        fields = ("id", "email", "password", "first_name", "last_name", *PROFILE_FIELDS)

    @transaction.atomic
    def create(self, validated_data):
        profile_data = {f: validated_data.pop(f) for f in PROFILE_FIELDS if f in validated_data}
        user = User.objects.create_user(**validated_data)  # role defaults to resident
        Profile.objects.update_or_create(user=user, defaults=profile_data)
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = authenticate(
            request=self.context.get("request"),
            email=attrs["email"],
            password=attrs["password"],
        )
        if user is None:
            raise serializers.ValidationError("Invalid email or password.")
        attrs["user"] = user
        return attrs


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "first_name", "last_name", "role")
        read_only_fields = ("id", "email", "role")


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    def validate_old_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect.")
        return value

    def validate_new_password(self, value):
        validate_password(value, self.context["request"].user)
        return value