from flask import request, Flask
from flask_restplus import Resource, Api

# local import
from bucketlist.models import User
from bucketlist import db


class CreateUser(Resource):

    def post(self):
        """.. :quickref: User Authentication; Register a new user

        .. sourcecode:: http

          POST /auth/register/ HTTP/1.1
          Host: localhost:5000
          Accept: application/json

        :reqheader Accept: application/json
        :<json string name: username
        :<json string email: user email
        :<json string password: user password

        :resheader Content-Type: application/json
        :status 200: user created
        :status 422: invalid parameters
        """
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
    """.. :quickref: User Authentication; User Log in

        .. sourcecode:: http

          POST /auth/login/ HTTP/1.1
          Host: localhost:5000
          Accept: application/json

        :reqheader Accept: application/json
        :<json string email: user email
        :<json string password: user password


        :resheader Content-Type: application/json
        :resheader Location: bucketlist url
        :status 200: successfully logged in
        :status 422: invalid parameters
        """

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


def make_port():
    """Creates api access port."""

    app = Flask(__name__)
    api = Api(app)

    api.add_resource(CreateUser, '/auth/register')
    api.add_resource(LogUserIn, '/auth/login')
    return app
