import pytest

from api import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True

    app_context = app.test_request_context()
    app_context.push()

    client = app.test_client()

    yield client
