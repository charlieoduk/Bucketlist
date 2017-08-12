import json

from flask_testing import TestCase

from bucketlist import app, db


class BaseTestCase(TestCase):
    """ Base Tests """

    def create_app(self):
        app.config.from_object('bucketlist.config.TestingConfig')
        return app

    def register_user(self, name, email, password):
        return self.client.post(
            '/api/v1.0/auth/register/',
            data=json.dumps(dict(
                name=name,
                email=email,
                password=password
            )),
            content_type='application/json',
        )

    def base_registration(self):
        return self.register_user('Joe', 'joe@gmail.com', '123456')

    def login_user(self, email, password):
        return self.client.post(
            '/api/v1.0/auth/login/',
            data=json.dumps(dict(
                email=email,
                password=password
            )),
            content_type='application/json',
        )

    def base_authentication(self):
        self.base_registration()
        login = self.login_user(
            email='joe@gmail.com', password='123456')
        token = json.loads(login.data.decode())
        user_token = token['token']
        return user_token

    def base_add_bucketlist(self):
        user_token = self.base_authentication()
        self.client.post(
            '/api/v1.0/bucketlists/',
            data=json.dumps(dict(
                name="new bucketlist",
            )), headers={'Authorization': user_token},
        )

    def base_add_bucketlist2(self):
        user_token = self.base_authentication()
        self.client.post(
            '/api/v1.0/bucketlists/',
            data=json.dumps(dict(
                name="Second bucketlist",
            )), headers={'Authorization': user_token},
        )

    def base_add_item(self):
        user_token = self.base_authentication()
        self.base_add_bucketlist()

        self.client.post(
            '/api/v1.0/bucketlists/1/items/',
            data=json.dumps(dict(
                name="Bungee jump",
            )), headers={'Authorization': user_token},
        )

    def setUp(self):
        db.create_all()
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
