import os

from flask import Flask

from config import config_by_name
from application.apis import create_apis
from application.models import db

def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_by_name[config_name])

    app.logger.info('Connecting database')
    db.init_app(app)

    @app.route('/', methods=['GET'])
    def index():
        return '<a href="https://github.com/danilolmoura/ze-api#api-documentação">Read the docs!</a>'

    app.logger.info('creating apis')
    from flask_potion import Api

    api = Api(app, prefix='/api/v1', title='Zé API')
    create_apis(api)

    app.logger.info('Finished initialization')

    return app
