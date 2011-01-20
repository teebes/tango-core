import unittest

from flaskext.testing import TestCase

from tango.factory import build_app


class AppInitTestCase(TestCase):

    def create_app(self):
        return build_app('tango.site.default')

    def setUp(self):
        self.client = self.app.test_client()

    def tearDown(self):
        pass

    def testStatic(self):
        response = self.client.get('/static/images/willowtree-avatar.png')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()