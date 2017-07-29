from flask import request, jsonify
from flask_restplus import Resource, fields, marshal_with
from sqlalchemy import desc

# local import
from bucketlist import db
from bucketlist.models import Bucketlist, Item, User

item_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'date_created': fields.DateTime(attribute='date_created'),
    'date_modified': fields.DateTime(attribute='date_modified'),
    'done': fields.Boolean
}


class ItemsResource(Resource):

    def post(self, bucketlist_id):
        token = request.headers.get('Authorization')
        if token:
            current_user = User.verify_auth_token(token)
        else:
            return {'message': 'Unauthorized Access!'}
        if current_user:
            arguments = request.get_json(force=True)
            name = arguments.get('name')

            bucketlist = db.session.query(Bucketlist).filter_by(
                created_by=current_user.id, id=bucketlist_id)
            if bucketlist:
                item = Item(name=name, bucketlist_id=bucketlist_id)
                item.save()

                return {'message': 'Item successfully added to bucketlist'}
            else:
                return {'message': 'Bucketlist not found'}
        else:
            return {'message': 'Expired or invalid token'}


class ItemsList(Resource):

    def put(self, bucketlist_id, item_id):
        token = request.headers.get('Authorization')
        if token:
            current_user = User.verify_auth_token(token)
        else:
            return {'message': 'Unauthorized Access!'}
        if current_user:
            arguments = request.get_json(force=True)
            name, done = arguments.get('name') or None, arguments.get('done')

            bucketlist = Bucketlist.query.filter_by(
                id=bucketlist_id).first()

            if bucketlist:
                item = Item.query.filter_by(
                    id=item_id, bucketlist=bucketlist).first()
                if item:
                    item.name = name if name is not None else item.name
                    item.done = done if done is not None else item.done
                    item.save()
                else:
                    {'message': 'Item not found'}
            else:
                return {'message': 'Bucketlist not found'}
        else:
            return {'message': 'Expired or invalid token'}

    def delete(self, bucketlist_id, item_id):
        token = request.headers.get('Authorization')
        if token:
            current_user = User.verify_auth_token(token)
        else:
            return {'message': 'Unauthorized Access!'}
        if current_user:
            bucketlist = Bucketlist.query.filter_by(
                id=bucketlist_id).first()

            if bucketlist:
                item = Item.query.filter_by(
                    id=item_id, bucketlist=bucketlist).first()
                if item:
                    item.delete()
                    return {'message': 'Successfully deleted Item'}
                else:
                    {'message': 'Item not found'}
        else:
            return {'message': 'Expired or invalid token'}
