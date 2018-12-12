import os


class BaseSettings:
    FLASK_ENV = os.environ["FLASK_ENV"]
    FLASK_APP = os.environ["FLASK_APP"]
    FLASK_DEBUG = os.environ["FLASK_DEBUG"]
    MONGODB_SETTINGS = {"host": os.environ["MONGODB_URI"]}
    SECRET_KEY = os.environ["SECRET_KEY"]
