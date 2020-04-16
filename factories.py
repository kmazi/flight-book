from datetime import timedelta

import factory
from django.utils import timezone
from factory.fuzzy import FuzzyChoice, FuzzyDate

from api import models
from user.models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Faker("email")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    username = factory.Faker("first_name")
    password = factory.Faker("password")


class FlightFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Flight

    origin = factory.Faker("city")
    destination = factory.Faker("city")
    departure_date = FuzzyDate(timezone.now().date(),
                               end_date=timezone.now().date() +
                               timedelta(weeks=52))
    plane_type = FuzzyChoice(["economic", "business", "first_class"])
