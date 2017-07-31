from flask import request
from flask_restplus import Resource, fields, marshal_with, abort, marshal, reqparse

from bucketlist.bucketlists.parsers import parser
# local import
from bucketlist.models import Bucketlist, BucketListItems, User
from bucketlist.items.views import item_fields
from bucketlist import db

bucketlist_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'items': fields.Nested(item_fields),
    'date_created': fields.DateTime(attribute='date_created'),
    'date_modified': fields.DateTime(attribute='date_modified'),
    'created_by': fields.Integer(attribute='created_by')
}


class BucketListResource(Resource):
    """Bucketlists Collection."""

    @marshal_with(bucketlist_fields)
    def get(self):
        '''Returns a collection of bucketlists that belong to the user

        .. :quickref: BucketListResource; Get a collection of Bucketlists

        **Example request**:

        .. sourcecode:: http

          GET /posts/ HTTP/1.1
          Host: example.com
          Accept: application/json

        **Example response**:

        .. sourcecode:: http

          HTTP/1.1 200 OK
          Vary: Accept
          Content-Type: application/json

        [
            {
                "id": 8,
                "name": "numero 2",
                "items": [
                    {
                        "id": 3,
                        "name": "build a snow man",
                        "date_created": "2017-07-28T16:14:27.477147",
                        "date_modified": "2017-07-28T16:14:27.477076",
                        "done": false
                    }
                ],
                "date_created": "2017-07-28T16:14:57.853548",
                "date_modified": "2017-07-28T16:14:57.853548",
                "created_by": 2
            },
            {
                "id": 7,
                "name": "Awesome list",
                "items": [
                    {
                        "id": 4,
                        "name": "monaco reloaded",
                        "date_created": "2017-07-28T16:14:27.477147",
                        "date_modified": "2017-07-29T15:57:05.707369",
                        "done": true
                    }
                ],
                "date_created": "2017-07-28T15:26:14.349677",
                "date_modified": "2017-07-29T16:25:58.765675",
                "created_by": 2
            }
        ]

        :resheader Content-Type: application/json
        :status 200: posts found

        '''
        token = request.headers.get('Authorization')
        if token:
            current_user = User.verify_auth_token(token)
        else:
            abort(400, message='Unauthorized Access!')

        if not isinstance(current_user,User):
            abort(401, current_user)

        # get arguments

        # arguments = parser.parse_args(request)
        # q = arguments.get("q")
        # limit = arguments.get("limit")
        # page = arguments.get("page")


        bucketlists = db.session.query(
            Bucketlist).filter_by(created_by=current_user.id).all()

        if bucketlists:
            # return marshal(bucketlists)
            return marshal(bucketlists, bucketlist_fields)
            # hateos
        abort(
            400, message='Bucketlist not found or does not belong to you.'
        )


    def post(self):
        '''Adds a new bucketlist'''
        token = request.headers.get('Authorization')
        if token:
            current_user = User.verify_auth_token(token)
        else:
            abort(400, message='Unauthorized Access!')
        if current_user:
            arguments = request.get_json(force=True)
            try:
                name = arguments['name']
            except:
                return {'message':'Invalid parameter entered'}
            bucketlists = db.session.query(Bucketlist).all()
            current_bucketlists = []

            if not name:
                # we return bad request since we require name
                return {'message': 'Missing required parameters.'}, 400
            for bucketlist in bucketlists:
                current_bucketlists.append(bucketlist.name)
            if name not in current_bucketlists:
                new_bucketlist = Bucketlist(
                    name=name, created_by=current_user.id)
                new_bucketlist.save()

                return {'message': 'successfully added a new bucketlist'}
            return {'message': 'bucketlist already exists'}
        else:
            abort(400, message='Expired or invalid token')


class BucketListItemsResource(Resource):

    @marshal_with(bucketlist_fields)
    def get(self, bucketlist_id):
        '''Displays a bucketlist specified by the id'''
        token = request.headers.get('Authorization')
        if token:
            current_user = User.verify_auth_token(token)
        else:
            abort(400, message='Unauthorized Access!')
        if current_user:
            bucketlistitem = db.session.query(
                Bucketlist).filter_by(created_by=current_user.id, id=bucketlist_id).first()
            if not bucketlistitem:
                abort(404, message='Bucketlist not found')
            else:
                return bucketlistitem
        else:
            abort(400, message='Expired or invalid token')

    def put(self, bucketlist_id):
        '''Update the name of the bucketlist'''
        token = request.headers.get('Authorization')
        if token:
            current_user = User.verify_auth_token(token)
        else:
            return {'message': 'Unauthorized Access!'}
        if current_user:
            arguments = request.get_json(force=True)
            name = arguments.get('name')

            bucketlist = Bucketlist.query.filter_by(
                created_by=current_user.id, id=bucketlist_id).first()
            if bucketlist:
                bucketlist.name = name
                bucketlist.save()
                return {'message': 'Successfully updated the bucketlist'}
            else:
                return{'message': 'Could not find bucketlist'}
        else:
            return {'message': 'Expired or invalid token'}

    def delete(self, bucketlist_id):
        ''''''
        token = request.headers.get('Authorization')
        if token:
            current_user = User.verify_auth_token(token)
        else:
            return {'message': 'Unauthorized Access!'}
        if current_user:
            bucketlist = Bucketlist.query.filter_by(
                created_by=current_user.id, id=bucketlist_id).first()

            if bucketlist:
                bucketlist.delete()
                return {'message': 'Bucketlist successfully deleted'}
            else:
                return {'message': 'Could not find bucketlist'}
        else:
            return {'message': 'Expired or invalid token'}
