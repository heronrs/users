from mongoengine import (
    BooleanField,
    DateField,
    Document,
    EmailField,
    EmbeddedDocumentField,
    ListField,
    StringField,
)

from api.utils import CustomBaseQuerySet

from .address import Address


class User(Document):

    meta = {"queryset_class": CustomBaseQuerySet}

    first_name = StringField(max_length=80, required=True)
    last_name = StringField(max_length=80, required=True)
    cpf = StringField(max_length=80, unique=True, required=True)
    birthdate = DateField(required=True)
    address = EmbeddedDocumentField(Address, required=True)
    telephones = ListField(field=StringField(), required=True)
    emails = ListField(field=EmailField())
    active = BooleanField(default=True)
