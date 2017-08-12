import unittest

from flask_testing import TestCase

from bucketlist import app


class TestDevelopmentConfig(TestCase):

    def create_app(self):
        app.config.from_object('bucketlist.config.DevelopmentConfig')
        return app

    def test_app_is_development(self):
        self.assertTrue(app.config['DEBUG'])
        self.assertTrue(
            app.config[
                'SQLALCHEMY_DATABASE_URI'] == 'postgresql://localhost/bucketlist'
        )


class TestTestingConfig(TestCase):

    def create_app(self):
        app.config.from_object('bucketlist.config.TestingConfig')
        return app

    def test_app_is_testing(self):
        self.assertTrue(app.config['DEBUG'])
        self.assertTrue(
            app.config[
                'SQLALCHEMY_DATABASE_URI'] == 'postgresql://localhost/bucketlist_test'
        )


class TestProductionConfig(TestCase):

    def create_app(self):
        app.config.from_object('bucketlist.config.ProductionConfig')
        return app

    def test_app_is_production(self):
        self.assertFalse(app.config['DEBUG'])


if __name__ == '__main__':
    unittest.main()
