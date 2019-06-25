"""Define view for handling auth operations."""

from django.contrib.auth import get_user_model
from rest_framework import views
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .serializers import UserSerializer


class UserViewSet(ModelViewSet):
    """Define registration endpoint."""
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)
    http_method_names = ("post", "get", "patch",)


class LoginView(views.APIView):
    """Define login functionality."""

    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        """Handle post request when login in."""
        return Response()
