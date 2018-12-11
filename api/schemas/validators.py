import re

from marshmallow import ValidationError


# https://wiki.python.org.br/VerificadorDeCpfCnpjSimples
def cpf_validator(cpf):
    cpf = "".join(re.findall(r"\d", str(cpf)))

    if (not cpf) or (len(cpf) < 11):
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
