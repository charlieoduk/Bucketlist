from flask import request, jsonify
from flask_restplus import Resource


# local import
from bucketlist.models import Bucketlist, BucketListItems, User
from bucketlist import db


class BucketListResource(Resource):

    def get(self):
        '''Lists all the bucketlists available'''
        token = request.headers.get('Authorization')
        if token:
            current_user = User.verify_auth_token(token)
        else:
            return {'message': 'Unauthorized Access!'}
        if current_user:
            bucketlists = db.session.query(
                Bucketlist).filter_by(created_by=current_user.id)
            if not bucketlists:
                return {'message': 'Not Found'}, 404
            bucketlistsfromdb = []
            for bucketlist in bucketlists:
                bucketlistsfromdb.append({
                    "id": bucketlist.id,
                    "name": bucketlist.name,
                    "items": bucketlist.items,
                    "date_created": bucketlist.date_created,
                    "date_modified": bucketlist.date_modified,
                    "created_by": current_user.name.capitalize()
                })
            return jsonify(bucketlistsfromdb)
        else:
            return {'message': 'Expired or invalid token'}

    def post(self):
        '''Adds a new bucketlist'''
        token = request.headers.get('Authorization')
        if token:
            current_user = User.verify_auth_token(token)
        else:
            return {'message': 'Unauthorized Access!'}
        if current_user:
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
                    name=name, created_by=current_user.id)
                new_bucketlist.save()

                return {'message': 'successfully added a new bucketlist'}
            return {'message': 'bucketlist already exists'}
        else:
            return {'message': 'Expired or invalid token'}


class BucketListItemsResource(Resource):

    def get(self, bucketlist_id):
        '''Displays a bucketlist specified by the id'''
        token = request.headers.get('Authorization')
        if token:
            current_user = User.verify_auth_token(token)
        else:
            return {'message': 'Unauthorized Access!'}
        if current_user:
            bucketlistitem = db.session.query(
                Bucketlist).filter_by(created_by=current_user.id, id=bucketlist_id).first()
            bucketlistfromdb = []
            if not bucketlistitem:
                return {'message': 'No bucketlist items found'}, 404
            else:
                bucketlistfromdb.append({
                    "id": bucketlistitem.id,
                    "name": bucketlistitem.name,
                    "items": bucketlistitem.items,
                    "date_created": bucketlistitem.date_created,
                    "date_modified": bucketlistitem.date_modified,
                    "created_by": current_user.name.capitalize()
                })
                return jsonify(bucketlistfromdb)
        else:
            return {'message': 'Expired or invalid token'}

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

            bucketlist = Bucketlist.query.filter_by(created_by=current_user.id,id=bucketlist_id).first()
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
            bucketlist = Bucketlist.query.filter_by(created_by=current_user.id, id=bucketlist_id).first()

            if bucketlist:
                bucketlist.delete()
                return {'message': 'Bucketlist successfully deleted'}
            else:
                return {'message': 'Could not find bucketlist'}
        else:
            return {'message': 'Expired or invalid token'}
