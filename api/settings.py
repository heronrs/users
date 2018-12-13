import os


class BaseSettings:
    FLASK_ENV = os.environ["FLASK_ENV"]
    FLASK_APP = os.environ["FLASK_APP"]
    FLASK_DEBUG = os.environ["FLASK_DEBUG"]
    MONGODB_SETTINGS = {"host": os.environ["MONGODB_URI"]}
    SECRET_KEY = os.environ["SECRET_KEY"]


LOGGING = {
    "version": 1,
    "formatters": {
        "default": {
            "format": "[%(asctime)s] %(levelname)s in %(name)s: %(message)s",
            "class": "pythonjsonlogger.jsonlogger.JsonFormatter",
        }
    },
    "handlers": {
        "wsgi": {
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
            "formatter": "default",
        }
    },
    "loggers": {
        "flask": {"handlers": ["wsgi"], "level": os.environ.get("LOG_LEVEL", "INFO")},
        "gunicorn.error": {
            "handlers": ["wsgi"],
            "level": os.environ.get("LOG_LEVEL", "INFO"),
        },
        "gunicorn.access": {
            "handlers": ["wsgi"],
            "level": os.environ.get("LOG_LEVEL", "INFO"),
        },
    },
}
