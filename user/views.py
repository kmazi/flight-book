"""Define view for handling auth operations."""

import logging

from django.contrib.auth import authenticate, get_user_model
from rest_framework import status, views
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import UserSerializer

logger = logging.getLogger(__name__)
logging.basicConfig(level="ERROR", format="[%(asctime)s] <=>|| %(message)s")


class UserViewSet(ModelViewSet):
    """Define registration endpoint."""
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny, )
    http_method_names = (
        "post",
        "get",
        "patch",
    )


class LoginView(views.APIView):
    """Define login functionality."""

    permission_classes = (AllowAny, )

    def post(self, request, *args, **kwargs):
        """Handle post request when login in."""
        data = {
            "username": request.data.get("username"),
            "password": request.data.get("password")
        }
        response = {}
        user = authenticate(request, **data)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            token = {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "id": refresh["user_id"]
            }
            logger.info("Login was successful for: %s", user.username)
            response = {"username": user.username, **token}
            status_code = status.HTTP_200_OK
        else:
            response = {"error": "Invalid credentials"}
            status_code = status.HTTP_403_FORBIDDEN
        return Response(data=response, status=status_code)
