"""Define view classes."""

from django.contrib.auth import get_user_model
from django.http import response
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from .filters import FlightFilter
from .models import Flight, Booking
from .permissions import AllowAuthenicUserPatch, IsAdminWriteOnly
from .serializers import FlightSerializer

from rest_framework.views import APIView


class FlightViewset(APIView):
    
    def get_object(self, id):
        return Flight.records.get(id=id)

    def patch(self, request, id):
        flight = self.get_object(id)
        User = get_user_model()
 
        print(request._user.id)
        try:
            user = User.objects.get(pk=request._user.id)
            print(user)
        except Exception:
            return Response(
                data={"error": "An invalid user is trying to book a flight"},
                status=status.HTTP_400_BAD_REQUEST)
        else:

            if flight.passengers.filter(username=request._user.username).exists():
                raise ValidationError(
                    detail="Flight has already been booked by you")

            if flight.passengers.count() > flight.capacity:
                raise ValidationError(
                detail="The flight has been fully booked")

            result = flight.passengers.add(user)
            serializer = FlightSerializer(result)
            return Response(data=serializer.data, status=status.HTTP_200_OK)

@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny, ))
def home(request):
    """Handle default request."""
    return Response(data="Welcome to flightbookie..")
