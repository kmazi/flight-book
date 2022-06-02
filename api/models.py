from datetime import timedelta

from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone


# Create your models here.
class Plane(models.Model):
    manufacturer = models.CharField(max_length=256, blank=False, null=False)
    name = models.CharField(max_length=256, blank=False, null=False)
    model = models.CharField(max_length=256, blank=False, null=False)
    capacity = models.IntegerField(blank=False, null=False, default=0)


class Flight(models.Model):
    """Flight model definition."""

    ECONOMIC = "economic"
    BUSINESS = "business"
    FIRST_CLASS = "first_class"
    FLIGHT_TYPES = [
        (ECONOMIC, "economic class"),
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

    plane = models.ForeignKey(Plane, on_delete=models.SET_NULL, null=True)

    records = models.Manager()
