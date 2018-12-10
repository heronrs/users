from api.models import User
from marshmallow import fields
from marshmallow_mongoengine import ModelSchema


class UserSchema(ModelSchema):
    birthdate = fields.Date(required=True)

    class Meta:
        model = User
