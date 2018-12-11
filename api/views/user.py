from flask import Blueprint, current_app, jsonify, request
from webargs import fields
from webargs.flaskparser import use_args, use_kwargs

from api.models import User
from api.schemas import UserSchema, make_user_schema
from api.utils import APIException

view = Blueprint("users", __name__, url_prefix="/api/users")


@view.route("/", methods=["GET"])
@use_args(
    {
        "page": fields.Int(missing=1),
        "per_page": fields.Int(missing=10),
        "first_name": fields.String(attribute="first_name__iexact"),
        "last_name": fields.String(attribute="last_name__iexact"),
        "cpf": fields.String(),
    },
    locations=("query",),
)
def list(args):
    page, per_page = args.pop("page"), args.pop("per_page")
    paginator = User.objects.filter(**args).paginate(page=page, per_page=per_page)

    schema = UserSchema(many=True)
    result = schema.dump(paginator.items)

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
