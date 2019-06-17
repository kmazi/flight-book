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
    return_date = models.DateField()
    departure_date = models.DateField()
    plane_type = models.CharField(max_length=100,
                                  choices=FLIGHT_TYPES,
                                  default=ECONOMIC)

    records = models.Manager()
