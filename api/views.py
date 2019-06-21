"""Define view classes."""

from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny

from .filters import FlightFilter
from .models import Flight
from .serializers import FlightSerializer


# Create your views here.
class FlightViewset(ModelViewSet):
    """Flight viewset."""

    queryset = Flight.records.all()
    serializer_class = FlightSerializer
    filterset_class = FlightFilter


@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def home(request):
    """Handle default request."""
    return Response(data="Welcome to flightbookie..")
