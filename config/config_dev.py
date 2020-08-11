import os

from . import Config

class ConfigDev(Config):
    DEVELOPMENT = True
    DEBUG = True
    FLASK_ENV = 'dev'
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{}:{}@{}/{}'.format(
        os.environ['POSTGRES_ZE_USER_API_DEV'],
        os.environ['POSTGRES_ZE_PASSWORD_API_DEV'],
        os.environ['POSTGRES_ZE_SERVER_API_DEV'],
        os.environ['POSTGRES_ZE_DB_API_DEV'],
    )
