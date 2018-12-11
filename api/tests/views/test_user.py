import json

from bson.objectid import ObjectId
from flask import url_for

from api.conftest import StubFactory
from api.models import User
from api.schemas import UserSchema


def test_list_user(client):
    StubFactory.create_user()
    StubFactory.create_user(
        {"first_name": "Jane", "last_name": "Dunninghan", "cpf": "3768851100"}
    )

    resp = client.get(url_for("users.list"))

    user_1 = resp.json["result"][0]
    user_2 = resp.json["result"][1]

    User.objects.get(**user_1).id == user_1["id"]
    User.objects.get(**user_2).id == user_2["id"]

    assert len(resp.json["result"]) == 2
    assert resp.status_code == 200


def test_create_user(client):
    user = StubFactory.create_user(save_db=False)
    schema = UserSchema()
    result = schema.dumps(user)

    resp = client.post(
        url_for("users.create"), data=result.data, content_type="application/json"
    )

    User.objects.get(**resp.json)

    assert resp.status_code == 201


def test_create_user_bulk(client):
    user1 = StubFactory.create_user(save_db=False)
    user2 = StubFactory.create_user(
        {"first_name": "Jane", "last_name": "Dunninghan", "cpf": "3768851100"},
        save_db=False,
    )

    schema = UserSchema(many=True)
    result = schema.dumps([user1, user2])

    resp = client.post(
        url_for("users.create"), data=result.data, content_type="application/json"
    )

    user1 = resp.json[0]
    user2 = resp.json[1]

    User.objects.get(**user1)
    User.objects.get(**user2)

    assert resp.status_code == 201


def test_get_user(client):
    user = StubFactory.create_user(save_db=True)
    resp = client.get(url_for("users.get", user_id=user.id))

    assert User.objects.get(**resp.json).id == user.id
    assert resp.status_code == 200


def test_get_user_not_found(client):
    _id = str(ObjectId())
    resp = client.get(url_for("users.get", user_id=_id))

    assert resp.status_code == 404
    assert resp.json == {"message": "Resource not found () {'id': '%s'}" % _id}


def test_delete_user(client):
    user = StubFactory.create_user(save_db=True)
    resp = client.delete(url_for("users.delete", user_id=user.id))

    assert len(User.objects.filter(id=user.id)) == 0
    assert resp.status_code == 204


def test_update_user(client):
    user = StubFactory.create_user(save_db=True)
    user_data = {"first_name": "Tony", "last_name": "Soprano"}

    resp = client.patch(
        url_for("users.update", user_id=user.id),
        data=json.dumps(user_data),
        content_type="application/json",
    )

    assert User.objects.get(**user_data).id == user.id
    assert resp.status_code == 204


def test_remove_user(client):
    user = StubFactory.create_user(save_db=True)
    assert User.objects.get(id=user.id).active is True

    resp = client.post(url_for("users.remove", user_id=user.id))

    assert User.objects.get(id=user.id).active is False
    assert resp.status_code == 201
