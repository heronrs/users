from logging.config import dictConfig

from flask import Flask, jsonify, cli


from .utils import LOGGING, APIException
from .views.user import view as user_view


def create_app():
    dictConfig(LOGGING)

    app = Flask(__name__)

    cli.load_dotenv()

    from .settings import BaseSettings

    app.config.from_object(BaseSettings)

    app.register_blueprint(user_view)

    @app.errorhandler(APIException)
    def handle_invalid_usage(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    return app
