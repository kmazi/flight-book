from datetime import timedelta

from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone


# Create your models here.

"""
Plane Model:
    plane : CharField
    number_of_seats : IntergarField
"""
class Plane(models.Model):
    name = models.CharField(max_length=512, default=None, null=True, blank=True)
    number_of_seats = models.IntegerField(default=50)

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
    passengers = models.ManyToManyField(get_user_model())
    plane_type = models.CharField(max_length=100,
                                  choices=FLIGHT_TYPES,
                                  default=ECONOMIC)
    records = models.Manager()
    """
    Add plane to flight model :FK to Plane Model
    """
    plane = models.ForeignKey(Plane, on_delete=models.CASCADE, null=True, default=None, blank=True)
# create a model for plane