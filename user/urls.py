"""Define urls for user auth."""

from rest_framework import routers
from django.urls import path
from .views import UserViewSet, LoginView


router = routers.DefaultRouter()
router.register(r"users", UserViewSet, basename="user")

urlpatterns = [
  path(r"login", LoginView.as_view(), name="login")
]

urlpatterns += router.urls
