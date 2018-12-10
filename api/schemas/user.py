from api.models.user import User
from marshmallow_mongoengine import ModelSchema
from marshmallow import fields


class UserSchema(ModelSchema):
    birthdate = fields.Date(required=True)

    class Meta:
        model = User
