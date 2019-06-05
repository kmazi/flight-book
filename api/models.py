from django.db import models


# Create your models here.
class Flight(models.Model):

    ECONOMIC = "economic"
    BUSINESS = "business"
    FIRST_CLASS = "first_class"
    FLIGHT_TYPES = [
        (ECONOMIC, "econimic class"),
        (BUSINESS, "business class"),
        (FIRST_CLASS, "first class"),
    ]
    name = models.CharField(max_length=100)
    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    return_date = models.DateField(null=True)
    departure_date = models.DateField(null=True)
    plane_type = models.CharField(max_length=100,
                                  choices=FLIGHT_TYPES,
                                  default=FLIGHT_TYPES[0][0])

    records = models.Manager()
