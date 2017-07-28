import json
import unittest

from bucketlist.models import User
from tests.base import BaseTestCase as base


class TestAuthBlueprint(base):

    def test_registration(self):
        """ Test for user registration """
        response = base.base_registration(self)
        data = json.loads(response.data.decode())
        self.assertTrue(data['message'] == 'Successfully added a user')
        self.assertEqual(response.status_code, 201)

    def test_register_user_twice(self):
        """Test if registering the same user twice returns an error"""
        user = User(name='joe', email='joe@gmail.com',
                    password='123456')
        user.save()
        response = base.base_registration(self)
        data = json.loads(response.data.decode())
        self.assertTrue(data['message'] == 'Failed!! User already exists')
        self.assertEqual(response.status_code, 200)
        user.delete()


if __name__ == '__main__':
    unittest.main()
