import pytest

from api import create_app
from pymongo import MongoClient
from api.models.address import Address
from api.models.user import User


@pytest.fixture
def app():
    app = create_app()
    app.config["TESTING"] = True

    app_context = app.test_request_context()
    app_context.push()

    yield app

    teardown_database(app)


@pytest.fixture
def client(app):
    client = app.test_client()

    yield client


def teardown_database(app):
    db_uri = app.config["MONGODB_SETTINGS"]["host"]
    db_name = app.config["MONGODB_SETTINGS"]["host"][::-1].split("/")[0][::-1]

    connection = MongoClient(db_uri)
    connection.drop_database(db_name)


class StubFactory:
    @staticmethod
    def create_user(data=None):
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
            "cpf": "35411126744",
            "birthdate": "2010-10-28",
            "telephones": ["551622338877", "551633448977"],
            "address": address_data,
        }
        user_data.update(**data or {})

        return User(**user_data).save().reload()

    @staticmethod
    def create_address(data=None):
        address_data = {
            "city": "São Carlos",
            "state_province": "SP",
            "country": "Brazil",
            "zip_code": "14801180",
            "public_area_desc": "Av Lapena",
            "number": "877",
        }
        address_data.update(**data or {})

        return Address(**address_data)
