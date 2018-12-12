from marshmallow import fields
from marshmallow_mongoengine import ModelSchema

from api.models import User
from api.schemas.validators import cpf_validator


class UserSchema(ModelSchema):
    birthdate = fields.Date(required=True)
    cpf = fields.String(validate=cpf_validator, required=True)

    class Meta:
        model = User
