import pytest


@pytest.fixture
def user(db_transaction):
    """
    Create a test user.
    """
    from django.contrib.auth.models import User
    user = User.objects.create_user('test', 'test@github.com', 'test')
    return user
