import os

from flask import Flask

from config import config_by_name
from .models import db

def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_by_name[config_name])

    app.logger.info('Connecting database')
    db.init_app(app)

    @app.route('/', methods=['GET'])
    def index():
        return 'Hello Zé Delivery'

    app.logger.info('Finished initialization')

    return app
