import json
import unittest

from tests.base import BaseTestCase as base


class TestItems(base):

    def test_add_item(self):
        user_token = base.base_authentication(self)
        base.base_add_bucketlist(self)

        response = self.client.post(
            '/api/v1.0/bucketlists/1/items/',
            data=json.dumps(dict(
                name="Sky dive",
            )), headers={'Authorization': user_token},
        )

        data = json.loads(response.data.decode())
        self.assertEqual(
            data['message'], 'Item successfully added to bucketlist')

    def test_authorization_required(self):
        base.base_add_bucketlist(self)

        response = self.client.post(
            '/api/v1.0/bucketlists/1/items/',
            data=json.dumps(dict(
                name="Sky dive",
            ))
        )

        data = json.loads(response.data.decode())
        self.assertEqual(
            data['message'], 'Unauthorized Access!')

    def test_update_item(self):
        user_token = base.base_authentication(self)
        base.base_add_item(self)

        update = self.client.put(
            '/api/v1.0/bucketlists/1/items/1/',
            data=json.dumps(dict(
                name="Climb mount kenya",
            )), headers={'Authorization': user_token},
        )
        data = json.loads(update.data.decode())
        self.assertEqual(data['message'], 'Successfully updated the item')

    def test_delete_item(self):
        user_token = base.base_authentication(self)
        base.base_add_item(self)

        delete = self.client.delete(
            '/api/v1.0/bucketlists/1/items/1/',
            headers={'Authorization': user_token},
        )
        data = json.loads(delete.data.decode())
        self.assertEqual(data['message'], 'Successfully deleted Item')


if __name__ == '__main__':
    unittest.main()
