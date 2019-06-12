from django_filters import rest_framework as filters

from .models import Flight


class FlightFilter(filters.FilterSet):
    departure_date = filters.DateFilter(field_name="departure_date")
    # return_date = filters.DateFilter(field_name="return_date",
    #                                  lookup_expr='iexact')

    class Meta:
        model = Flight
        fields = ["departure_date"]
