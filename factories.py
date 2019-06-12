from datetime import datetime as dt
from datetime import timedelta

import factory
from factory.fuzzy import FuzzyChoice, FuzzyDate

from api import models
from user.models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Faker("email")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    username = factory.Faker("username")
    password = factory.Faker("password")


class FlightFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Flight

    origin = factory.Faker("city")
    destination = factory.Faker("city")
    return_date = FuzzyDate(dt.today().date(),
                            end_date=dt.today().date() + timedelta(weeks=52))
    departure_date = FuzzyDate(dt.today().date(),
                               end_date=dt.today().date() +
                               timedelta(weeks=52))
    plane_type = FuzzyChoice(["economic", "business", "first_class"])
