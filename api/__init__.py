from logging.config import dictConfig

from flask import Flask, jsonify, cli
from flask_mongoengine import MongoEngine

from .exceptions import APIException
from .blueprints import user


def create_app():
    cli.load_dotenv()

    from .settings import BaseSettings, LOGGING

    dictConfig(LOGGING)

    app = Flask(__name__)
    app.config.from_object(BaseSettings)
    app.url_map.strict_slashes = False

    configure_blueprints(app)
    configure_extensions(app)
    configure_error_handlers(app)

    return app


def configure_blueprints(app):
    app.register_blueprint(user, url_prefix='/api/v1/users')


def configure_extensions(app):
    db = MongoEngine()
    db.init_app(app)


def configure_error_handlers(app):
    @app.errorhandler(APIException)
    def handle_invalid_usage(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response
