"""Define view for handling auth operations."""

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from .serializers import UserSerializer


class UserViewSet(ModelViewSet):
    """Define registration endpoint."""
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)
    http_method_names = ("post", "get", "patch",)
