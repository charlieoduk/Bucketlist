from flask import request, jsonify, g
from flask_restful import reqparse, Resource, fields

# local import
from .models import Bucketlist, BucketListItems, User
from .config import db, api, app, auth


class BucketListResource(Resource):

    @auth.login_required
    def get(self):
        '''Lists all the bucketlists available'''
        current_user = g.user
        bucketlists = db.session.query(
            Bucketlist).filter_by(user=current_user)
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

    @auth.login_required
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
            new_bucketlist.save()

            return {'message': 'successfully added a new bucketlist'}
        return {'message': 'bucketlist already exists'}


class BucketListItemsResource(Resource):

    @auth.login_required
    def get(self, bucketlist_id):
        bucketlistitem = db.session.query(
            BucketListItems).filter_by(bucketlist_id=bucketlist_id)
        if not bucketlistitem:
            return {'message': 'No bucketlist items found'}, 404

    @auth.login_required
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
        new_bucketlist.save()
        return {new_bucketlist.id: {'name': bucketlist.name, 'date_created': bucketlist.color}}, 201


api.add_resource(BucketListResource, '/bucketlists/')
api.add_resource(BucketListItemsResource, '/bucketlists/<int:bucketlist_id>/')
