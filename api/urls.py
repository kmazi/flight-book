"""Define routes for endpoints."""

from rest_framework import routers
from .views import FlightViewset


router = routers.SimpleRouter()
router.register(r"flights", FlightViewset, basename="flight")
