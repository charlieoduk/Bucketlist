import os

from flask import Flask
from flask_httpauth import HTTPBasicAuth
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api

from .config import app_config

# initialize sql-alchemy
db = SQLAlchemy()
# initialize HTTP auth
auth = HTTPBasicAuth()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(app_config[config_name])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    from bucketlist.auth import auth as auth_blueprint
    api = Api(auth_blueprint)
    app.register_blueprint(auth_blueprint, url_prefix='/api/v1')
    from bucketlist.auth.views import CreateUser, LogUserIn
    api.add_resource(CreateUser, '/auth/register/')
    api.add_resource(LogUserIn, '/auth/login/')

    return app


app = create_app(config_name=os.getenv('APP_SETTINGS'))
test_app = create_app(config_name='testing')
