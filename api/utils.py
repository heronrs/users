from flask_mongoengine import BaseQuerySet
from mongoengine.errors import DoesNotExist


class CustomBaseQuerySet(BaseQuerySet):
    def get_or_raise(self, *args, **kwargs):
        try:
            return self.get(*args, **kwargs)

        except DoesNotExist:
            raise APIException(
                "Resource not found %s %s" % (args, kwargs), status_code=404
            )


class APIException(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        super().__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv["message"] = self.message
        return rv


LOGGING = {
    "version": 1,
    "formatters": {
        "default": {
            "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
            "class": "pythonjsonlogger.jsonlogger.JsonFormatter",
        }
    },
    "handlers": {
        "wsgi": {
            "class": "logging.StreamHandler",
            "stream": "ext://flask.logging.wsgi_errors_stream",
            "formatter": "default",
        }
    },
    "root": {"level": "INFO", "handlers": ["wsgi"]},
}
