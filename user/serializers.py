"""Define serializers for custom user model."""

from rest_framework import serializers
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """User serializer definition."""

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
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validate_data):
        """Create a user."""
        user = UserModel.objects.create(username=validate_data["username"],
                                        email=validate_data["email"],
                                        first_name=validate_data["first_name"],
                                        last_name=validate_data["last_name"])
        user.set_password(validate_data["password"])
        user.save()
        return user
