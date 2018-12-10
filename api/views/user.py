from flask import Blueprint, jsonify

view = Blueprint("users", __name__, url_prefix="/api/users")


@view.route("/", methods=["GET"])
def list():
    return jsonify({"action": "LIST"})


@view.route("/", methods=["POST"])
def create():
    return jsonify({"action": "CREATE"})


@view.route("/<user_id>/", methods=["GET"])
def get(user_id):
    return jsonify({"action": "GET"})


@view.route("/<user_id>/", methods=["DELETE"])
def delete(user_id):
    return jsonify({"action": "DELETE"})


@view.route("/<user_id>/", methods=["PUT", "PATCH"])
def update(user_id):
    return jsonify({"action": "PUT, PATCH"})
