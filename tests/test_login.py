import json
import unittest

from bucketlist.models import User
from tests.base import BaseTestCase as base


class TestAuthLogin(base):

    def test_registered_user_login(self):

        response = base.base_registration(self)
        data = json.loads(response.data.decode())
        self.assertEqual(data['message'], 'Successfully added a user')

        response = base.login_user(
            self, email='joe@gmail.com', password='123456')
        data = json.loads(response.data.decode())
        self.assertEqual(data['message'], 'Successfully logged in')

    def test_unregistered_user_login(self):

        response = base.login_user(
            self, email='unknown@gmail.com', password='123')
        data = json.loads(response.data.decode())
        self.assertTrue(data['message'] ==
                        'User does not exist or incorrect password')


if __name__ == '__main__':
    unittest.main()
