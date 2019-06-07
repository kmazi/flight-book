"""Define view classes."""

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from .models import Flight
from .serializer import FlightSerializer


# Create your views here.
class FlightViewset(ModelViewSet):
    """Flight viewset."""

    queryset = Flight.records.all()
    serializer_class = FlightSerializer
    permission_classes = (AllowAny,)
