import os


class BaseSettings:
    FLASK_ENV = os.environ["FLASK_ENV"]
    FLASK_APP = os.environ["FLASK_APP"]
    FLASK_DEBUG = os.environ["FLASK_DEBUG"]
