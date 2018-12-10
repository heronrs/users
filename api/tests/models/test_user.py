import pytest
from mongoengine.errors import ValidationError

from api.models.user import User


def test_can_create_user(client):
    address = {
        "city": "São Carlos",
        "state_province": "SP",
        "country": "Brazil",
        "zip_code": "14801180",
        "public_area_desc": "Av Lapena",
        "number": "877",
    }

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

    assert user_data["first_name"] == User.objects.first().to_mongo()["first_name"]
    assert user_data["emails"] == User.objects.first().to_mongo()["emails"]


def test_can_create_user_without_emails(client):
    address = {
        "city": "São Carlos",
        "state_province": "SP",
        "country": "Brazil",
        "zip_code": "14801180",
        "public_area_desc": "Av Lapena",
        "number": "877",
    }

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

    assert user_data["first_name"] == User.objects.first().to_mongo()["first_name"]
    assert user_data["telephones"] == User.objects.first().to_mongo()["telephones"]


def test_cannot_create_user_required_fields(client):

    user_data = {}

    user = User(**user_data)
    with pytest.raises(
        ValidationError,
        match="['first_name', 'last_name', 'cpf', 'birthdate', 'address'], ['telephones']",
    ):
        user.save()
