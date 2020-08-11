import os

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ['SECRET_KEY']
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    POTION_DEFAULT_PER_PAGE = 20
    POTION_MAX_PER_PAGE = 5000

config_by_name = dict(
    dev='config.config_dev.ConfigDev',
    test='config.config_test.ConfigTest',
)
