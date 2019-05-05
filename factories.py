from datetime import datetime as dt

import factory
from factory.fuzzy import FuzzyInteger

from api import models
from user.models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    id = factory.sequence(lambda a: a)
    email = factory.Faker('email')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    password = factory.Faker('password')


class FlightFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Flight

    id = factory.sequence(lambda a: a)
    name = factory.Faker('first_name')
    origin = factory.sequence(lambda a: f'Lagos{a}')
    destination = factory.Faker('address')
    departure_time = dt.strptime(
        factory.Faker('time').generate({}), "%H:%M:%S").time()
    departure_date = dt.strptime(
        factory.Faker('date').generate({}), "%Y-%m-%d").date()
    number = FuzzyInteger(12322)
