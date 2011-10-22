import unittest

from flaskext.testing import TestCase

from tango.app import Tango
from tango.shelf import BaseConnector


class BaseConnectorTestCase(TestCase):

    def create_app(self):
        return Tango(__name__)

    def setUp(self):
        self.connector = BaseConnector(self.app)

    def tearDown(self):
        pass

    def test_app_init(self):
        # Sub-classes rely on this attribute in the base class.
        self.assertEqual(self.connector.app, self.app)
        self.assertEqual(self.connector.app.config, self.app.config)

    def test_get_notimplemented(self):
        self.assertRaises(NotImplementedError, self.connector.get, '', '')

    def test_put_notimplemented(self):
        self.assertRaises(NotImplementedError, self.connector.put, '', '', {})


if __name__ == '__main__':
    unittest.main()
