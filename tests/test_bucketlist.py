import json
import unittest

from tests.base import BaseTestCase as base


class TestAddBucketlist(base):

    def test_login_required(self):
        base.base_authentication(self)
        response = self.client.post(
            '/api/v1.0/bucketlists/',
            data=json.dumps(dict(
                name="new bucketlist",
            ))
        )

        data = json.loads(response.data.decode())
        self.assertEqual(data['message'], 'Unauthorized Access!')

    def test_add_new_bucketlist(self):
        user_token = base.base_authentication(self)
        response = self.client.post(
            '/api/v1.0/bucketlists/',
            data=json.dumps(dict(
                name="new bucketlist",
            )), headers={'Authorization': user_token},
        )

        data = json.loads(response.data.decode())
        self.assertEqual(
            data['message'], 'successfully added a new bucketlist')

    def test_add_existing_bucketlist(self):
        user_token = base.base_authentication(self)
        base.base_add_bucketlist(self)

        response = self.client.post(
            '/api/v1.0/bucketlists/',
            data=json.dumps(dict(
                name="new bucketlist",
            )), headers={'Authorization': user_token},
        )
        data = json.loads(response.data.decode())
        self.assertEqual(data['message'], 'bucketlist already exists')

    def test_unnamed_bucetlist(self):
        user_token = base.base_authentication(self)
        response = self.client.post(
            '/api/v1.0/bucketlists/',
            data=json.dumps(dict(
                name="",
            )), headers={'Authorization': user_token},
        )

        data = json.loads(response.data.decode())
        self.assertEqual(data['message'], 'Missing required parameters.')

    def test_pass_invalid_parameter(self):
        user_token = base.base_authentication(self)
        response = self.client.post(
            '/api/v1.0/bucketlists/',
            data=json.dumps(dict(
                email="new@gmail.com"
            )), headers={'Authorization': user_token},
        )

        data = json.loads(response.data.decode())
        self.assertEqual(data['message'], 'Invalid parameter entered')

    def test_get_all_bucketlists(self):
        user_token = base.base_authentication(self)
        base.base_add_bucketlist(self)
        base.base_add_bucketlist2(self)

        response = self.client.get(
            '/api/v1.0/bucketlists/',
            headers={'Authorization': user_token},
        )
        self.assertIn('new bucketlist', str(response.data))
        self.assertIn('Second bucketlist', str(response.data))

    def test_get_bucketlist_by_id(self):
        user_token = base.base_authentication(self)
        base.base_add_bucketlist(self)

        response = self.client.get(
            '/api/v1.0/bucketlists/1/',
            headers={'Authorization': user_token},
        )
        self.assertIn('new bucketlist', str(response.data))

    def test_update_bucketlist(self):
        user_token = base.base_authentication(self)
        base.base_add_bucketlist(self)

        response = self.client.put(
            '/api/v1.0/bucketlists/1/',
            data=json.dumps(dict(
                name="revised bucketlist"
            )),
            headers={'Authorization': user_token},
        )

        data = json.loads(response.data.decode())
        self.assertEqual(
            data['message'], 'Successfully updated the bucketlist')

    def test_delete_bucketlist(self):
        user_token = base.base_authentication(self)
        base.base_add_bucketlist(self)

        response = self.client.delete(
            '/api/v1.0/bucketlists/1/',
            headers={'Authorization': user_token},
        )

        data = json.loads(response.data.decode())
        self.assertEqual(data['message'], 'Bucketlist successfully deleted')


if __name__ == '__main__':
    unittest.main()
