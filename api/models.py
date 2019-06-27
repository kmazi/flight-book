from datetime import datetime, timedelta

from django.contrib.auth import get_user_model
from django.db import models


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
    return_date = models.DateField(default=datetime.today().date() +
                                   timedelta(days=3))
    departure_date = models.DateField(default=datetime.today().date() +
                                      timedelta(days=1))
    passengers = models.ManyToManyField(get_user_model())
    plane_type = models.CharField(max_length=100,
                                  choices=FLIGHT_TYPES,
                                  default=ECONOMIC)

    records = models.Manager()
