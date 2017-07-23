import time
import json
import unittest

from bucketlist import db
from bucketlist.models import User
from tests.base import BaseTestCase


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


def login_user(self, email, password):
    return self.client.post(
        '/api/v1/auth/login/',
        data=json.dumps(dict(
            email=email,
            password=password
        )),
        content_type='application/json',
    )


class TestAuthBlueprint(BaseTestCase):

    def test_registration(self):
        """ Test for user registration """
        with self.client:
            response = register_user(self, 'Joe', 'joe@gmail.com', '123456')
            data = json.loads(response.data.decode())
            self.assertTrue(data['message'] == 'Successfully added a user')
            self.assertEqual(response.status_code, 201)


if __name__ == '__main__':
    unittest.main()
