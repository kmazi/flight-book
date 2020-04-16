from django_filters import rest_framework as filters

from .models import Flight


class FlightFilter(filters.FilterSet):
    departure = filters.DateFilter(field_name="departure_date")

    class Meta:
        model = Flight
        fields = ["departure_date"]
