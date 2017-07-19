from flask import request, jsonify
from flask_httpauth import HTTPBasicAuth
from flask_restful import reqparse, Resource, fields

# local import
from .models import Bucketlist, BucketListItems, User
from .config import db, api, app

auth = HTTPBasicAuth()


class CreateUser(Resource):

    def post(self):
        '''Creates a new user'''
        arguments = request.get_json(force=True)

        if not arguments['name'] or not arguments['password'] or not arguments['email']:
            # we return bad request since we require name, email and password
            return {'message': 'Missing required parameters.'}, 400

        name = arguments['name']
        email = arguments['email']
        password = arguments['password']

        new_user = User(
            name=name, password=password, email=email)
        db.session.add(new_user)
        db.session.commit()
        # return a success message
        return {'message': 'Successfully added a user'}


class LogUserIn(Resource):
    '''Checks if user exists then log them in'''

    def get(self):
        return {'message': 'This route works'}


class BucketListResource(Resource):

    def get(self):
        '''Lists all the bucketlists available'''
        bucketlists = db.session.query(
            Bucketlist).all()
        if not bucketlists:
            return {'message': 'Not Found'}, 404
        bucketlistsfromdb = []
        for bucketlist in bucketlists:
            bucketlistsfromdb.append({
                "id": bucketlist.id,
                "name": bucketlist.name,
                "items": [],
                "date_created": bucketlist.date_created,
                "date_modified": bucketlist.date_modified,
                "created_by": bucketlist.created_by
            })
        return jsonify(bucketlistsfromdb)

    def post(self):
        '''Adds a new bucketlist'''
        arguments = request.get_json(force=True)
        name = arguments['name']
        bucketlists = db.session.query(Bucketlist).all()
        current_bucketlists = []

        if not name:
            # we return bad request since we require name
            return {'message': 'Missing required parameters.'}, 400
        for bucketlist in bucketlists:
            current_bucketlists.append(bucketlist.name)
        if name not in current_bucketlists:
            new_bucketlist = Bucketlist(
                name=name, created_by=1)
            db.session.add(new_bucketlist)
            db.session.commit()

            return {'message': 'successfully added a new bucketlist'}
        return {'message': 'bucketlist already exists'}


class BucketListItemsResource(Resource):

    def get(self, bucketlist_id):
        pass

    def post(self, bucketlist_id):
        parser = reqparse.RequestParser()
        parser.add_argument('name')
        parser.add_argument('date_created')
        args = parser.parse_args()
        if not 'name' in args or not 'date_created' in args:
            # we return bad request since we require name and color
            return {'message': 'Missing required parameters.'}, 400
        new_bucketlist = Bucketlist(
            name=args['name'], date_created=args['date_created'])
        db.session.add(new_bucketlist)
        db.session.commit()
        return {new_bucketlist.id: {'name': bucketlist.name, 'date_created': bucketlist.color}}, 201


api.add_resource(LogUserIn, '/auth/login/')
api.add_resource(CreateUser, '/auth/register/')
api.add_resource(BucketListResource, '/bucketlists/')
api.add_resource(BucketListItemsResource, '/bucketlists/<int:bucketlist_id>/')
