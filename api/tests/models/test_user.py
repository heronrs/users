import pytest
from mongoengine.errors import ValidationError

from api.conftest import StubFactory
from api.models import User


def test_can_create_user(client):
    address = StubFactory.create_address()

    user_data = {
        "first_name": "John",
        "last_name": "Doe",
        "cpf": "35411126744",
        "birthdate": "2010-10-28",
        "telephones": ["551622338877", "551633448977"],
        "emails": ["johndoe@example.com", "johnydoe@example2.com"],
        "address": address,
    }

    user = User(**user_data)
    user.save()

    assert user_data["first_name"] == User.objects.first().first_name
    assert user_data["emails"] == User.objects.first().emails


def test_can_create_user_without_emails(client):
    address = StubFactory.create_address()

    user_data = {
        "first_name": "John",
        "last_name": "Doe",
        "cpf": "35411126744",
        "birthdate": "2010-10-28",
        "telephones": ["551622338877", "551633448977"],
        "address": address,
    }

    user = User(**user_data)
    user.save()

    assert user_data["last_name"] == User.objects.first().last_name
    assert user_data["telephones"] == User.objects.first().telephones


def test_cannot_create_user_required_fields(client):

    user_data = {}

    user = User(**user_data)
    with pytest.raises(
        ValidationError,
        match="['first_name', 'last_name', 'cpf', 'birthdate', 'address'], ['telephones']",
    ):
        user.save()
