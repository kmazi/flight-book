"""Define serializers for API."""

from rest_framework.serializers import ModelSerializer
from .models import Flight


class FlightSerializer(ModelSerializer):
    """flight object serializer."""

    class Meta:
        """Meta data for flight object."""

        model = Flight
        fields = ("id", "name", "origin", "destination", "departure_date",
                  "return_date", "plane_type")
