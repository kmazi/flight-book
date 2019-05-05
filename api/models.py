from django.db import models


# Create your models here.
class Flight(models.Model):
    name = models.CharField(max_length=100)
    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    departure_time = models.TimeField()
    departure_date = models.DateField(null=True)
    number = models.IntegerField()
