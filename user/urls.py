"""Define urls for user auth."""

from rest_framework import routers
from .views import UserViewSet, LoginViewSet


router = routers.SimpleRouter()
router.register(r"users", UserViewSet, basename="user")
router.register(r"login", LoginViewSet, basename="login")
