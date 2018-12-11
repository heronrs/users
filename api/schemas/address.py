from marshmallow_mongoengine import ModelSchema

from api.models import Address


class AddressSchema(ModelSchema):
    class Meta:
        model = Address
