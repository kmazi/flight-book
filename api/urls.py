"""Define routes for endpoints."""
from django.urls import include, path
from rest_framework import routers
from .views import FlightViewset

app_name = "api"


urlpatterns = [
    path("flights/<int:id>", FlightViewset.as_view(), name="flight")
]

router = routers.SimpleRouter()
#router.register(r"flights", FlightViewset.as_view(), basename="flight")
#router.register(r"flights/<int:id>", FlightViewset, basename="flight")
