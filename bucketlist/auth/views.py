from flask import request, g
from flask_restplus import Resource

# local import
from bucketlist.models import User
from bucketlist import db


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

        users = db.session.query(User).all()
        registered_emails = []

        for user in users:
            registered_emails.append(user.email)

        if email not in registered_emails:

            new_user = User(
                name=name, password=password, email=email)
            new_user.hash_password(password)
            new_user.save()
            # return a success message
            return {'message': 'Successfully added a user'}, 201

        return {'message': 'Failed!! User already exists'}


class LogUserIn(Resource):
    '''Checks if user exists then log them in'''

    def post(self):
        arguments = request.get_json(force=True)
        email = arguments['email']
        password = arguments['password']

        user = User.query.filter_by(email=email).first()
        if not user or not user.verify_password(password=password):
            return {'message': 'User does not exist or incorrect password'}
        token = user.generate_auth_token()
        return {
            'message': 'Successfully logged in',
            'token': token.decode('utf-8'),
        }
