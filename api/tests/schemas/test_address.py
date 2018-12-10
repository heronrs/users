import json

from api.conftest import StubFactory
from api.schemas import AddressSchema


def test_can_serialize_address(app):
    address = StubFactory.create_address()
    schema = AddressSchema()
    result = schema.dump(address)

    assert result.errors == {}
    assert json.dumps(result.data)


def test_can_deserialize_address(app):
    address_data = {
        "city": "São Carlos",
        "state_province": "SP",
        "country": "Brazil",
        "zip_code": "14801180",
        "public_area_desc": "Av Lapena",
        "number": "877",
    }

    schema = AddressSchema()
    result = schema.load(address_data)
    address = result.data

    assert result.errors == {}
    address.validate()


def test_cannot_deserialize_address_required_fields(app):
    address_data = {}

    schema = AddressSchema()
    result = schema.load(address_data)

    assert result.errors == {
        "city": ["Missing data for required field."],
        "country": ["Missing data for required field."],
        "state_province": ["Missing data for required field."],
        "number": ["Missing data for required field."],
        "public_area_desc": ["Missing data for required field."],
    }
