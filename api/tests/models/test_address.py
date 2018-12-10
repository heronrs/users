from api.models.address import Address
import json
import pytest
from mongoengine.errors import ValidationError


def test_can_create_address(client):
    address_data = {
        "city": "São Carlos",
        "state_province": "SP",
        "country": "Brazil",
        "zip_code": "14801180",
        "public_area_desc": "Av Lapena",
        "number": "877",
    }

    address = Address(**address_data)
    address.validate()

    assert address.to_json() == json.dumps(address_data)


def test_can_create_address_without_zip_code(client):
    address_data = {
        "city": "São Carlos",
        "state_province": "SP",
        "country": "Brazil",
        "public_area_desc": "Av Lapena",
        "number": "877",
    }

    address = Address(**address_data)
    address.validate()

    assert address.to_json() == json.dumps(address_data)


def test_cannot_create_addres_required_fields(client):
    address_data = {}

    address = Address(**address_data)
    with pytest.raises(
        ValidationError,
        match="['city', 'state_province', 'country', 'public_area_desc', 'number']",
    ):
        address.validate()

