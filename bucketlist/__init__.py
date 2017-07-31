import os

from flask import Flask
from flask_httpauth import HTTPTokenAuth
from flask_sqlalchemy import SQLAlchemy
from flask_restplus import Api

from .config import app_config

# initialize sql-alchemy
db = SQLAlchemy()
# initialize HTTP auth
authentication = HTTPTokenAuth(scheme='Token')


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(app_config[config_name])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)


    from bucketlist.auth import auth as auth_blueprint
    api = Api(auth_blueprint)
    app.register_blueprint(auth_blueprint, url_prefix='/api/v1.0')
    from bucketlist.auth.views import CreateUser, LogUserIn
    api.add_resource(CreateUser, '/auth/register/')
    api.add_resource(LogUserIn, '/auth/login/')

    from bucketlist.bucketlists import bucketlists as bucketlists_blueprint
    api = Api(bucketlists_blueprint)
    app.register_blueprint(bucketlists_blueprint, url_prefix='/api/v1.0')
    from bucketlist.bucketlists.views import BucketListItemsResource, BucketListResource
    api.add_resource(BucketListResource, '/bucketlists/')
    api.add_resource(BucketListItemsResource,
                     '/bucketlists/<int:bucketlist_id>/')

    from bucketlist.items import items as items_blueprint
    api = Api(items_blueprint)
    app.register_blueprint(items_blueprint, url_prefix='/api/v1.0')
    from bucketlist.items.views import ItemsResource, ItemsList
    api.add_resource(ItemsResource, '/bucketlists/<int:bucketlist_id>/items/')
    api.add_resource(ItemsList, '/bucketlists/<int:bucketlist_id>/items/<int:item_id>/')

    return app


app = create_app(config_name=os.getenv('APP_SETTINGS'))
