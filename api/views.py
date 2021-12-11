"""Define view classes."""

from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.viewsets import ModelViewSet

from .filters import FlightFilter
from .models import Flight, Plane
from .permissions import AllowAuthenicUserPatch, IsAdminWriteOnly
from .serializers import FlightSerializer


# Create your views here.
class FlightViewset(ModelViewSet):
    """Flight viewset."""

    queryset = Flight.records.all()
    #permission_classes = (IsAuthenticatedOrReadOnly,
    #                      IsAdminWriteOnly | AllowAuthenicUserPatch)
    serializer_class = FlightSerializer
    filterset_class = FlightFilter

    @action(detail=True, methods=["patch"])
    def book_flight(self, request, pk=None):
        """Handle patch requests."""
        flight = self.get_object()
        User = get_user_model()
        user_name = request.data["username"]
        departure_date = request.data["departure_date"]
        try:
            user = User.objects.get(username=user_name)
        except Exception:
            return Response(
                data={"error": "An invalid user is trying to book a flight"},
                status=status.HTTP_400_BAD_REQUEST)
        else:
            if flight.passengers.filter(username=user_name, departure_date=departure_date).exists():
                raise ValidationError(
                    detail="Flight has already been booked by you")

            else:
                plane = request.data["plane"]
                plane = Plane.objects.get(id=plane)
                seats_available = plane.capacity
                #                                                                                                                                                                                                                                                                              number = Flight.records.filter(plane_type__icontains="economic").count()
                if seats_available == Flight.records.all():
                    return Response(
                        data={"error": "The flight has been fully booked"},
                        status=status.HTTP_400_BAD_REQUEST)

                flight.passengers.add(user)
                serializer = self.get_serializer(flight)
                #plane.capacity -=1
                #plane.save()
                return Response(data=serializer.data, status=status.HTTP_200_OK)


@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny, ))
def home(request):
    """Handle default request."""
    return Response(data="Welcome to flightbookie..")
