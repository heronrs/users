from mongoengine import EmbeddedDocument, StringField


class Address(EmbeddedDocument):
    city = StringField(max_length=150, required=True)
    state_province = StringField(max_length=4, required=True)
    country = StringField(max_length=50, required=True)
    zip_code = StringField(max_length=15)
    public_area_desc = StringField(max_length=500, required=True)
    number = StringField(max_length=10, required=True)
