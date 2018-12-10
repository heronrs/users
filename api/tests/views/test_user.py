from flask import url_for


def test_list_user(client):
    resp = client.get(url_for("users.list"))
    assert resp.json == {"action": "LIST"}


def test_create_user(client):
    resp = client.post(url_for("users.create", user_id=123))
    assert resp.json == {"action": "CREATE"}


def test_get_user(client):
    resp = client.get(url_for("users.get", user_id=123))
    assert resp.json == {"action": "GET"}


def test_update_user(client):
    resp = client.put(url_for("users.update", user_id=123))
    assert resp.json == {"action": "PUT, PATCH"}


def test_delete_user(client):
    resp = client.delete(url_for("users.delete", user_id=123))
    assert resp.json == {"action": "DELETE"}
