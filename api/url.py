"""Define routes for endpoints."""

from rest_framework import routers
from .views import FlightViewset


router = routers.SimpleRouter()
router.register(r"flight/reservation", FlightViewset, basename="flight")
