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
            '/api/v1/auth/register/',
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
            '/api/v1/auth/login/',
            data=json.dumps(dict(
                email=email,
                password=password
            )),
            content_type='application/json',
        )

    def setUp(self):
        db.create_all()
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
