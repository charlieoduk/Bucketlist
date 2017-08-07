from flask import request, Flask
from flask_restplus import Resource, fields, marshal_with, abort, marshal, reqparse, Api
from flask_sqlalchemy import BaseQuery

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
        '''

        .. :quickref: Bucketlists Collection; List all the created bucket lists

        **Example request**:

        .. sourcecode:: http

          GET /bucketlists/ HTTP/1.1
          Host: localhost:5000
          Accept: application/json
          Authentication: <token>

        **Example response**:

        .. sourcecode:: http

          HTTP/1.1 200 OK
          Vary: Accept
          Content-Type: application/json

          [
            {
                "id": 1,
                "name": "Before 30",
                "items": [
                    {
                        "id": 1,
                        "name": "Sky Dive",
                        "date_created": "2017-07-30T22:29:10.044464",
                        "date_modified": "2017-07-31T10:13:44.926045",
                        "done": false
                    }
                ],
                "date_created": "2017-07-30T21:36:32.754289",
                "date_modified": "2017-07-30T21:36:32.754289",
                "created_by": 1
            },
            {
                "id": 2,
                "name": "Before 50",
                "items": [
                    {
                        "id": 2,
                        "name": "Climb Mt.Everest",
                        "date_created": "2017-08-07T06:39:22.466605",
                        "date_modified": "2017-08-07T06:39:22.466537",
                        "done": false
                    }

                ],
                "date_created": "2017-07-30T22:28:54.824647",
                "date_modified": "2017-07-30T22:28:54.824647",
                "created_by": 1
            },
          ]

        :query q: full text search query
        :query limit: number of bucket lists per page
        :query page: select page
        :resheader Content-Type: application/json
        :status 200: bucketlists found


        '''
        token = request.headers.get('Authorization')
        if token:
            current_user = User.verify_auth_token(token)
        else:
            abort(401, message='Unauthorized Access!')

        if not isinstance(current_user, User):
            abort(401, current_user)

        # get arguments
        parser = reqparse.RequestParser()
        parser.add_argument('q', type=str, required=False, location='args')
        parser.add_argument('limit', type=int, required=False,
                            default=20, help='Results per page',
                            location='args')
        parser.add_argument('page', type=int, default=1,
                            help='Page number', required=False,
                            location='args')

        arguments = parser.parse_args(request)
        q = arguments.get("q")
        limit = arguments.get("limit")
        page = arguments.get("page")

        if q:
            bucketlists = db.session.query(
                Bucketlist.name.ilike('%' + q + '%')).filter_by(
                created_by=current_user.id).paginate(
                page, limit, False)
        else:
            bucketlists = db.session.query(
                Bucketlist).filter_by(created_by=current_user.id).all()

        if bucketlists:
            # return marshal(bucketlists)
            return marshal(bucketlists, bucketlist_fields)
        abort(
            400, message='Bucketlists not found'
        )

    def post(self):
        """.. :quickref: Bucketlists Collection; Create a new bucket list.

        .. sourcecode:: http

          POST /bucketlists/1/ HTTP/1.1
          Host: localhost:5000
          Accept: application/json
          Authentication: <token>


        :reqheader Accept: application/json
        :reqheader Authentication: <token>

        :<json string name: bucketlist name


        :resheader Content-Type: application/json
        :status 201: bucketlist created
        :status 422: invalid parameters
        """

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
                return {'message': 'Invalid parameter entered'}
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
        '''.. :quickref: Bucketlist; Get single bucket list

        **Example request**:

        .. sourcecode:: http

          GET /bucketlists/1/ HTTP/1.1
          Host: localhost:5000
          Accept: application/json


        **Example response**:

        .. sourcecode:: http

          HTTP/1.1 200 OK
          Vary: Accept
          Content-Type: application/json
          Authentication: Token

          [
            {
                "id": 1,
                "name": "Before 50",
                "items": [
                    {
                        "id": 1,
                        "name": "Watch F1",
                        "date_created": "2017-07-30T22:29:10.044464",
                        "date_modified": "2017-07-31T10:13:44.926045",
                        "done": true
                    }

                ],
                "date_created": "2017-07-30T21:36:32.754289",
                "date_modified": "2017-07-30T21:36:32.754289",
                "created_by": 1
            },
          ]

        :resheader Content-Type: application/json
        :status 200: bucketlist found
        '''
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
        '''.. :quickref: Bucketlist; Update this bucket list
        .. sourcecode:: http

           PUT /bucketlists/1/ HTTP/1.1
           Host: localhost:5000
           Accept: application/json
           Authentication: <token>

        :<json string name: Edited bucketlist name

        :resheader Content-Type: application/json
        :status 200: bucketlist updated
        :status 422: invalid parameters

        '''
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
        '''.. :quickref: Bucketlist; Delete this single bucket list

        .. sourcecode:: http

          DELETE /bucketlists/1/ HTTP/1.1
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
                bucketlist.delete()
                return {'message': 'Bucketlist successfully deleted'}
            else:
                return {'message': 'Could not find bucketlist'}
        else:
            return {'message': 'Expired or invalid token'}


def make_port():
    """Creates api access port."""

    app = Flask(__name__)
    api = Api(app)

    api.add_resource(BucketListResource, '/bucketlists/',)
    api.add_resource(BucketListItemsResource,
                     '/bucketlists/<int:bucketlist_id>/')
    return app
