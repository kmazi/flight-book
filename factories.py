import factory
from factory.fuzzy import FuzzyInteger
from user.models import User
from api import models


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
    departure_time = factory.Faker('time')
    departure_date = factory.Faker('date')
    number = FuzzyInteger(12322)
