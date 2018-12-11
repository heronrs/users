from flask import Blueprint, jsonify, current_app, request

from api.models import User
from api.schemas import UserSchema
from api.utils import APIException

view = Blueprint("users", __name__, url_prefix="/api/users")


@view.route("/", methods=["GET"])
def list():
    users = User.objects.all()
    schema = UserSchema(many=True)
    result = schema.dump(users)
    if not result.errors:
        return jsonify({"result": result.data}), 200

    else:
        current_app.logger.error(
            "Error while serializing User Model", extra={"errors": result.errors}
        )
        raise APIException(
            "Internal server error while processing your requests", status_code=500
        )


@view.route("/", methods=["POST"])
def create():
    many = False

    if isinstance(request.json, type([])):
        many = True

    schema = UserSchema(many=many)
    result = schema.load(request.json)

    if not result.errors:
        if many:
            for user in result.data:
                user.save()

        else:
            result.data.save()

        return jsonify(schema.dump(result.data).data), 201

    else:
        current_app.logger.error(
            "Error creating new User", extra={"errors": result.errors}
        )
        raise APIException(
            "Error processing your request", status_code=400, payload=result.errors
        )


@view.route("/<user_id>/", methods=["GET"])
def get(user_id):
    user = User.objects.get_or_raise(id=user_id)

    schema = UserSchema()
    result = schema.dump(user)

    return jsonify(result.data), 200


@view.route("/<user_id>/", methods=["DELETE"])
def delete(user_id):
    User.objects.get_or_raise(id=user_id).delete()

    return jsonify({}), 204


@view.route("/<user_id>/", methods=["PUT", "PATCH"])
def update(user_id):
    user = User.objects.get_or_raise(id=user_id)

    schema = UserSchema()
    errors = schema.validate(request.json, partial=True)

    if errors:
        raise APIException(
            "Error processing your request", status_code=400, payload=errors
        )

    user.update(**request.json)
    user.save()

    return jsonify({}), 204


@view.route("/<user_id>/remove", methods=["POST"])
def remove(user_id):
    user = User.objects.get_or_raise(id=user_id)

    user.update(active=False)
    user.save()

    return jsonify({}), 201
