from marshmallow import fields
from marshmallow_mongoengine import ModelSchema

from api.models import User


class UserSchema(ModelSchema):
    birthdate = fields.Date(required=True)

    class Meta:
        model = User


def make_user_schema(request):
    only = request.args.get("fields", None)
    partial = request.method == "PATCH"
    return UserSchema(only=only, partial=partial, context={"request": request})
