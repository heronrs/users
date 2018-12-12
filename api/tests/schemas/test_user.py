import json

from api.conftest import StubFactory
from api.schemas import UserSchema


def test_can_serialize_user(app):
    user = StubFactory.create_user(save_db=True)
    schema = UserSchema()

    result = schema.dump(user)

    assert result.errors == {}
    assert json.dumps(result.data)


def test_can_deserialize_user(app):
    address_data = {
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
        "cpf": "03709557062",
        "birthdate": "28/10/2010",
        "telephones": ["551622338877", "551633448977"],
        "address": address_data,
    }

    schema = UserSchema()

    result = schema.load(user_data)
    user = result.data

    assert result.errors == {}
    user.save()


def test_cannot_deserialize_user_required_fields(app):
    user_data = {"address": {}}

    schema = UserSchema()

    result = schema.load(user_data)

    assert result.errors == {
        "address": {
            "city": ["Missing data for required field."],
            "country": ["Missing data for required field."],
            "number": ["Missing data for required field."],
            "public_area_desc": ["Missing data for required field."],
            "state_province": ["Missing data for required field."],
        },
        "birthdate": ["Missing data for required field."],
        "cpf": ["Missing data for required field."],
        "first_name": ["Missing data for required field."],
        "last_name": ["Missing data for required field."],
    }
