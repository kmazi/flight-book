"""Define urls for user auth."""

from rest_framework import routers
from .views import UserViewSet


router = routers.DefaultRouter()
router.register(r"users", UserViewSet, base_name="user")
