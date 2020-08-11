import os

from . import Config

class ConfigTest(Config):
    DEVELOPMENT = True
    DEBUG = True
    TESTING = True
    FLASK_ENV = 'test'
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{}:{}@{}/{}'.format(
        os.environ['POSTGRES_ZE_USER_API'],
        os.environ['POSTGRES_ZE_PASSWORD_API'],
        os.environ['POSTGRES_ZE_SERVER_API'],
        os.environ['POSTGRES_ZE_DB_API_DEV'],
    )
