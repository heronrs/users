import re

from marshmallow import ValidationError, fields, validates
from marshmallow_mongoengine import ModelSchema

from api.models import User


class UserSchema(ModelSchema):
    birthdate = fields.Date(required=True)
    cpf = fields.String(required=True)
    telephones = fields.List(fields.String(max_length=15), required=True)

    class Meta:
        model = User

    @validates("telephones")
    def validate_telephones(self, value):
        for tel in value:
            non_numbers = re.findall(r"[^0-9]", tel)
            if non_numbers:
                raise ValidationError("this list field accepts numbers only")

        return value

    @validates("cpf")
    def cpf_validator(self, cpf):
        # https://wiki.python.org.br/VerificadorDeCpfCnpjSimples
        non_numbers = re.findall(r"[^0-9]", cpf)

        cpf = "".join(re.findall(r"\d", str(cpf)))

        if non_numbers:
            raise ValidationError("this field accepts numbers only")

        invalid_cpfs = []
        for x in range(10):
            invalid_cpfs.append("".join(str(x) for y in range(11)))

        if (not cpf) or (len(cpf) < 11) or (cpf in invalid_cpfs):
            raise ValidationError("invalid value")

        integers = list(map(int, cpf))
        new = integers[:9]

        while len(new) < 11:
            r = sum([(len(new) + 1 - i) * v for i, v in enumerate(new)]) % 11

            if r > 1:
                f = 11 - r
            else:
                f = 0
            new.append(f)

        if new == integers:
            return cpf

        raise ValidationError("invalid value")
