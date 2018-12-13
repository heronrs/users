from marshmallow_mongoengine import ModelSchema
from marshmallow import fields, validates, ValidationError
from api.models import Address
import re


class AddressSchema(ModelSchema):
    zip_code = fields.String(max_length=15)

    @validates("zip_code")
    def validate_zip_code(self, value):
        non_numbers = re.findall(r"[^0-9]", value)

        if non_numbers:
            raise ValidationError("this field accepts numbers only")

        return value

    class Meta:
        model = Address
