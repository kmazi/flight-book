"""Define routes for endpoints."""

from rest_framework import routers
from .views import FlightViewset


router = routers.SimpleRouter()
router.register(r"flight/reservations", FlightViewset, basename="flight")
