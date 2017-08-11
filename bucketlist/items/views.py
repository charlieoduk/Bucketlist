from flask import request, Flask
from flask_restplus import Resource, fields, abort, Api

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
        """.. :quickref: Bucketlists Collection; Add a new bucketlist item.

        .. sourcecode:: http

          POST /bucketlists/1/items/ HTTP/1.1
          Host: localhost:5000
          Accept: application/json
          Authentication: <token>

        :reqheader Accept: application/json

        :<json string id: bucketlist id
        :<json string name: bucketlist name


        :resheader Content-Type: application/json
        :status 201: bucketlist created
        :status 422: invalid parameters
        """
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
                try:
                    item = Item(name=name, bucketlist_id=bucketlist_id)
                    item.save()

                    response = {
                        'message': 'Item successfully added to bucketlist'}
                    return response
                except:
                    abort(message='Failed to create item')

            else:
                abort(message='Bucketlist not found')
        else:
            abort(message='Expired or invalid token')


class ItemsList(Resource):

    def put(self, bucketlist_id, item_id):
        '''.. :quickref: Bucketlist; Update this bucket list item
        .. sourcecode:: http

           PUT /bucketlists/1/items/1/ HTTP/1.1
           Host: localhost:5000
           Accept: application/json
           Authentication: <token>

        :<json string name: New item name

        :resheader Content-Type: application/json
        :status 200: Item updated
        :status 422: invalid parameters
        '''
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
                    return {'message': 'Successfully updated the item'}
                else:
                    abort(message='Item not found')
            else:
                abort(message='Bucketlist not found')
        else:
            abort(message='Expired or invalid token')

    def delete(self, bucketlist_id, item_id):
        '''.. :quickref: Bucketlist; Delete this single bucket list

        .. sourcecode:: http

          DELETE /bucketlists/1/items/1/ HTTP/1.1
          Host: localhost:5000
          Accept: application/json
          Authentication: <token>

        :resheader Content-Type: application/json
        :status 204: bucketlist deleted
        '''
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


def make_port():
    """Creates api access port."""

    app = Flask(__name__)
    api = Api(app)

    api.add_resource(ItemsResource, '/bucketlists/<int:bucketlist_id>/items')
    api.add_resource(
        ItemsList, '/bucketlists/<int:bucketlist_id>/items/<int:item_id>')
    return app
