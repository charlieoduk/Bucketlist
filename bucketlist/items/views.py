from flask import request
from flask_restplus import Resource, fields, abort

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
            abort(message='Unauthorized Access!')
        if current_user:
            arguments = request.get_json(force=True)
            name = arguments.get('name')

            bucketlist = db.session.query(Bucketlist).filter_by(
                created_by=current_user.id, id=bucketlist_id)
            if bucketlist:
                item = Item(name=name, bucketlist_id=bucketlist_id)
                item.save()

                response = {'message': 'Item successfully added to bucketlist'}
                return response
            else:
                abort(message='Bucketlist not found')
        else:
            abort(message='Expired or invalid token')


class ItemsList(Resource):

    def put(self, bucketlist_id, item_id):
        token = request.headers.get('Authorization')
        if token:
            current_user = User.verify_auth_token(token)
        else:
            abort(message='Unauthorized Access!!')
        if current_user:
            arguments = request.get_json(force=True)
            name, done = arguments.get('name'), arguments.get('done')

            bucketlist = Bucketlist.query.filter_by(
                created_by=current_user.id, id=bucketlist_id).first()

            if bucketlist:
                item = Item.query.filter_by(
                    id=item_id, bucketlist_id=bucketlist_id).first()
                if item:
                    item.name = name if name is not None else item.name
                    item.done = done if done is not None else item.done
                    item.save()
                    return {'message':'Successfully updated the item'}
                else:
                    abort(message='Item not found')
            else:
                abort(message='Bucketlist not found')
        else:
            abort(message='Expired or invalid token')

    def delete(self, bucketlist_id, item_id):
        token = request.headers.get('Authorization')
        if token:
            current_user = User.verify_auth_token(token)
        else:
            return {'message': 'Unauthorized Access!'}
        if current_user:
            bucketlist = Bucketlist.query.filter_by(
                created_by=current_user.id, id=bucketlist_id).first()

            if bucketlist:
                item = Item.query.filter_by(
                    id=item_id, bucketlist_id=bucketlist_id).first()
                if item:
                    item.delete()
                    response = {'message': 'Successfully deleted Item'}
                    return response, 200
                else:
                    abort(message='Item not found')
        else:
            abort(message='Expired or invalid token')
