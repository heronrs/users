from api.models import Address
from marshmallow_mongoengine import ModelSchema


class AddressSchema(ModelSchema):
    class Meta:
        model = Address
