"""Define view classes."""

from django.contrib.auth import get_user_model
from django.db.models.query import QuerySet
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework import serializers
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
    permission_classes = (IsAuthenticatedOrReadOnly,)
                        #   IsAdminWriteOnly | AllowAuthenicUserPatch)
    serializer_class = FlightSerializer
    filterset_class = FlightFilter

    @action(detail=True, methods=["patch"])
    def book_flight(self, request, pk=None):
        """Handle patch requests."""
        flight = self.get_object()
        User = get_user_model()
        # user_name = request.data["username"]
        user_name = request.user
        try:
            user = User.objects.get(username=user_name)
        except Exception:
            return Response(
                data={"error": "An invalid user is trying to book a flight"},
                status=status.HTTP_400_BAD_REQUEST)
        else:
            plane = request.data['plane']
            # if flight.passengers.filter(username=user_name).exists():
            if flight.passengers.filter(username=user_name).filter(plane=plane).exists():
                # raise ValidationError(
                #     detail="Flight has already been booked by you")
                queryset = flight.passengers.filter(username=user_name).filter(plane=plane)
                data = self.serializer_class(queryset)
                return Response(data)
            
            plane = Plane.objects.get(plane=plane)
            number_of_seats_availabe = plane.number_of_seats
            if number_of_seats_availabe < 1:
                return Response({"data":"Seat filled"}, status=status.HTTP_400_BAD_REQUEST)
            
            serializer =self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            number_of_seats_availabe -= 1
            plane.save()

            return Response(data=serializer.data, status=status.HTTP_201_CREATED)

            
            # flight.passengers.add(user)
            # serializer = self.get_serializer(flight)
            # return Response(data=serializer.data, status=status.HTTP_200_OK)
        

    """
        User makes flight request, payload = ["plane", "destination", "depature_date"]
          -  Will check if plane exists: Plane.objects,get(id or plane etc)
          -  Check if user has not booked with this plan before if user has booked return Flights details in response with message
          -  Then check number of available seats in plane : When a user books a flight, the number should reduce and if number of availabe
             seats = 0, then plane is filled if not go ahead to book flight and return flight details
    """


@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny, ))
def home(request):
    """Handle default request."""
    return Response(data="Welcome to flightbookie..")
