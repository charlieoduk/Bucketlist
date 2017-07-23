from flask import request, g
from flask_restful import Resource

# local import
from bucketlist.models import User


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
        new_user.hash_password(password)
        new_user.save()
        # return a success message
        return {'message': 'Successfully added a user'}, 201


class LogUserIn(Resource):
    '''Checks if user exists then log them in'''

    def post(self):
        arguments = request.get_json(force=True)
        email = arguments['email']
        password = arguments['password']

        user = User.query.filter_by(email=email).first()

        if not user or not user.verify_password(password):
            return {'message': 'User does not exist or incorrect password'}
        g.user = user

        return {
            'message': 'Successfully logged in',
        }
