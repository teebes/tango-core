import os
import tempfile
import unittest

from flaskext.testing import TestCase

from tango.app import Tango
from tango.shelf import SqliteConnector

from common_tests import ConnectorCommonTests


class SqliteConnectorTestCase(TestCase, ConnectorCommonTests):

    def create_app(self):
        return Tango(__name__)

    def setUp(self):
        _, self.temp_filepath = tempfile.mkstemp(suffix='.db')
        self.app.config['SQLITE_FILEPATH'] = self.temp_filepath
        self.connector = SqliteConnector(self.app)

    def tearDown(self):
        self.remove_tempfile()

    def remove_tempfile(self):
        try:
            os.unlink(self.temp_filepath)
        except OSError, e:
            # Error number is 2 when file does not exist.
            if e.errno != 2:
                # Re-raise error if it's anything but non-existent file.
                raise e

    def test_db_init(self):
        self.remove_tempfile()
        self.smoke_test('Test non-existent file.')

        self.remove_tempfile()
        open(self.temp_filepath, 'w').close()
        self.smoke_test('Test empty file.')


if __name__ == '__main__':
    unittest.main()
