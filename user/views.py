"""Define view for handling auth operations."""

from django.contrib.auth import authenticate, get_user_model
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from helper import get_logger

from .serializers import UserSerializer

logger = get_logger(__name__)


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


class LoginViewSet(ViewSet):
    """Define login functionality."""

    permission_classes = (AllowAny, )
    http_method_names = ("post", )

    def create(self, request, format=None):
        """Handle post request when login in."""
        data = {
            "username": request.data.get("username"),
            "password": request.data.get("password")
        }
        user = get_user_model().objects.filter(
            username=data["username"]).first()
        logger.info("The user attempting to logi exist? %s", user is not None)
        logger.info("The input username is: %s and password is: %s",
                    data["username"], data["password"])
        response = {}
        user = authenticate(request, **data)
        logger.warning("Did the user authenticate successfully? %s",
                       user is not None)
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
            logger.error(
                "An error has occured while login in. No user available")
            response = {"error": "Invalid credentials"}
            status_code = status.HTTP_403_FORBIDDEN
        return Response(data=response, status=status_code)
