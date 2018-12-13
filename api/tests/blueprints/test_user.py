import json

from bson.objectid import ObjectId
from flask import url_for

from api.conftest import StubFactory
from api.models import User
from api.schemas import UserSchema


def test_list_users(client):
    StubFactory.create_user()
    StubFactory.create_user(
        {"first_name": "Jane", "last_name": "Dunninghan", "cpf": "52203351039"}
    )

    resp = client.get(url_for("user.list"))

    user_1 = resp.json["result"][0]
    user_2 = resp.json["result"][1]

    User.objects.get(**user_1).id == user_1["id"]
    User.objects.get(**user_2).id == user_2["id"]

    assert len(resp.json["result"]) == 2
    assert resp.status_code == 200


def test_list_users_pagination(client):
    StubFactory.create_user()
    StubFactory.create_user(
        {"first_name": "Jane", "last_name": "Dunninghan", "cpf": "52203351039"}
    )
    StubFactory.create_user(
        {"first_name": "Nemo", "last_name": "Captain", "cpf": "61755397020"}
    )

    resp = client.get(url_for("user.list"), query_string={"page": 1, "per_page": 1})

    assert resp.json["count"] == 3
    assert resp.json["next"] == url_for("user.list", page=2, per_page=1)
    assert resp.json.get("previous") is None
    assert len(resp.json["result"]) == 1
    assert resp.status_code == 200

    resp = client.get(url_for("user.list"), query_string={"page": 2, "per_page": 1})

    assert resp.json["next"] == url_for("user.list", page=3, per_page=1)
    assert resp.json["previous"] == url_for("user.list", page=1, per_page=1)


def test_list_users_pagination_filtered(client):
    StubFactory.create_user(
        {"first_name": "Jane", "last_name": "Dunninghan", "cpf": "52203351039"}
    )
    StubFactory.create_user(
        {"first_name": "Jane", "last_name": "Captain", "cpf": "61755397020"}
    )

    resp = client.get(
        url_for("user.list"),
        query_string={"page": 2, "per_page": 1, "first_name": "Jane"},
    )

    assert resp.json.get("next") is None
    assert resp.json["previous"] == url_for(
        "user.list", page=1, per_page=1, first_name="Jane"
    )
    assert resp.status_code == 200
    assert len(resp.json["result"]) == 1


def test_list_filtered_user(client):
    user = StubFactory.create_user(
        {"first_name": "Jane", "last_name": "Dunninghan", "cpf": "52203351039"}
    )

    resp = client.get(url_for("user.list"), query_string={"first_name": "JaNe"})

    assert User.objects.get(id=user.id).first_name == "Jane"

    assert len(resp.json["result"]) == 1
    assert resp.status_code == 200

    resp = client.get(url_for("user.list"), query_string={"cpf": "52203351039"})

    assert User.objects.get(id=user.id).cpf == "52203351039"

    assert len(resp.json["result"]) == 1
    assert resp.status_code == 200

    resp = client.get(url_for("user.list"), query_string={"last_name": "DunninGHan"})

    assert User.objects.get(id=user.id).last_name == "Dunninghan"

    assert len(resp.json["result"]) == 1
    assert resp.status_code == 200

    resp = client.get(
        url_for("user.list"),
        query_string={
            "cpf": "52203351039",
            "first_name": "Jane",
            "last_name": "Dunninghan",
        },
    )

    user = User.objects.get(id=user.id)
    assert user.last_name == "Dunninghan"
    assert user.first_name == "Jane"
    assert user.cpf == "52203351039"

    assert len(resp.json["result"]) == 1
    assert resp.status_code == 200

    resp = client.get(url_for("user.list"), query_string={"last_name": "Not Found"})

    assert len(resp.json["result"]) == 0
    assert resp.status_code == 200


def test_create_user(client):
    user = StubFactory.create_user({"cpf": "37600750880"}, save_db=False)
    schema = UserSchema()
    payload = {"data": schema.dump(user).data}

    resp = client.post(
        url_for("user.create"),
        data=json.dumps(payload),
        content_type="application/json",
    )

    User.objects.get(**resp.json)

    assert resp.status_code == 201


def test_create_user_bulk(client):
    user1 = StubFactory.create_user({"cpf": "71188941097"}, save_db=False)
    user2 = StubFactory.create_user(
        {"first_name": "Jane", "last_name": "Dunninghan", "cpf": "37600750880"},
        save_db=False,
    )

    schema = UserSchema(many=True)
    payload = {"data": schema.dump([user1, user2]).data}

    resp = client.post(
        url_for("user.create"),
        data=json.dumps(payload),
        content_type="application/json",
    )

    user1 = resp.json[0]
    user2 = resp.json[1]

    User.objects.get(**user1)
    User.objects.get(**user2)

    assert resp.status_code == 201


def test_get_user(client):
    user = StubFactory.create_user(save_db=True)
    resp = client.get(url_for("user.get", user_id=user.id))

    assert User.objects.get(**resp.json).id == user.id
    assert resp.status_code == 200


def test_get_user_not_found(client):
    _id = str(ObjectId())
    resp = client.get(url_for("user.get", user_id=_id))

    assert resp.status_code == 404
    assert resp.json == {"message": "Resource not found () {'id': '%s'}" % _id}


def test_get_user_invalid_id(client):
    _id = 1234
    resp = client.get(url_for("user.get", user_id=_id))

    assert resp.status_code == 400
    assert resp.json == {"message": "Invalid values provided () {'id': '%s'}" % _id}


def test_update_user_patch(client):
    user = StubFactory.create_user(save_db=True)
    user_data = {"first_name": "Tony", "last_name": "Soprano"}

    resp = client.patch(
        url_for("user.update", user_id=user.id),
        data=json.dumps(user_data),
        content_type="application/json",
    )

    assert User.objects.get(**user_data).id == user.id
    assert resp.status_code == 204


def test_update_user_put(client):
    user1 = StubFactory.create_user(save_db=True)
    user_data = {
        "first_name": "Tony",
        "last_name": "Soprano",
        "cpf": "03709557062",
        "birthdate": "22/10/1956",
        "telephones": ["5516996101220", "551133351122"],
        "address": {
            "city": "New Jersey",
            "state_province": "New York",
            "country": "United States",
            "zip_code": "66888",
            "public_area_desc": "Dover Beaches South",
            "number": "877",
        },
    }

    resp = client.put(
        url_for("user.update", user_id=user1.id),
        data=json.dumps(user_data),
        content_type="application/json",
    )

    assert User.objects.get(**user_data).id == user1.id
    assert resp.status_code == 204


def test_remove_user(client):
    user = StubFactory.create_user(save_db=True)
    assert User.objects.get(id=user.id).active is True

    resp = client.post(url_for("user.remove", user_id=user.id))

    assert User.objects.get(id=user.id).active is False
    assert resp.status_code == 201
