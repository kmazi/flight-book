from datetime import datetime as dt

import factory
from factory.fuzzy import FuzzyDate, FuzzyChoice

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
    return_date = FuzzyDate(dt.now().date())
    departure_date = FuzzyDate(dt.now().date())
    plane_type = FuzzyChoice(["economic", "business", "first_class"])
