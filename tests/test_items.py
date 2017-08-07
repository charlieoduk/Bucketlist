import json
import unittest

from tests.base import BaseTestCase as base


class TestItems(base):

    def test_add_item(self):
        user_token = base.base_add_bucketlist(self)

        response = self.client.post(
            '/api/v1.0/bucketlists/1/items/',
            data=json.dumps(dict(
                name="Sky dive",
            )), headers={'Authorization': user_token},
        )

        bucketlist = self.client.get(
            '/api/v1.0/bucketlists/1/',
            headers={'Authorization': user_token},
        )

        data = json.loads(response.data.decode())
        self.assertEqual(
            data['message'], 'Item successfully added to bucketlist')
        self.assertIn('Sky dive', str(bucketlist.data))

    def test_add_item_to_non_existing_bucketlist(self):
        user_token = base.base_add_bucketlist(self)

        response = self.client.post(
            '/api/v1.0/bucketlists/2/items/',
            data=json.dumps(dict(
                name="Sky dive",
            )), headers={'Authorization': user_token},
        )

        data = json.loads(response.data.decode())
        self.assertEqual(
            data['message'], 'Failed to create item')

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
        user_token = base.base_add_item(self)

        update = self.client.put(
            '/api/v1.0/bucketlists/1/items/1/',
            data=json.dumps(dict(
                name="Climb mount kenya",
            )), headers={'Authorization': user_token},
        )
        data = json.loads(update.data.decode())
        self.assertEqual(data['message'], 'Successfully updated the item')

    def test_delete_item(self):
        user_token = base.base_add_item(self)

        update = self.client.delete(
            '/api/v1.0/bucketlists/1/items/1/',
            headers={'Authorization': user_token},
        )
        data = json.loads(update.data.decode())
        self.assertEqual(data['message'], 'Successfully deleted Item')


if __name__ == '__main__':
    unittest.main()
