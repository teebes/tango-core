import unittest

from flaskext.testing import TestCase

from tango.factory import build_app


class FiltersTestCase(TestCase):

    def create_app(self):
        return build_app('tango.site.default')

    def setUp(self):
        self.client = self.app.test_client()

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
