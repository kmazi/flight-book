from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone


# Create your models here.
class Flight(models.Model):
    """Flight model definition."""

    ECONOMIC = "economic"
    BUSINESS = "business"
    FIRST_CLASS = "first_class"
    FLIGHT_TYPES = [
        (ECONOMIC, "econimic class"),
        (BUSINESS, "business class"),
        (FIRST_CLASS, "first class"),
    ]
    id = models.AutoField(primary_key=True)
    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    departure_date = models.DateField(default=timezone.now().date() +
                                      timedelta(days=1))
    passengers = models.ManyToManyField(get_user_model(), through="Booking", related_name="flights")
    plane_type = models.CharField(max_length=100,
                                  choices=FLIGHT_TYPES,
                                  default=ECONOMIC)
    capacity = models.IntegerField(default=100)

    records = models.Manager()


class Booking(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="booked_users")
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name="bookings")
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
