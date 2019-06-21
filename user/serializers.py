"""Define serializers for custom user model."""

from rest_framework import serializers
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """User serializer definition."""

    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=True)

    class Meta:
        """Meta for user serializer."""

        model = UserModel
        fields = (
            "id",
            "first_name",
            "last_name",
            "username",
            "email",
            "password",
            "is_active",
            "is_staff",
        )
        read_only_fields = (
            "id",
            "is_active",
            "is_staff",
        )
