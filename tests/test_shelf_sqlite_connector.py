import os
import tempfile
import unittest

from flaskext.testing import TestCase

from tango.app import Tango
from tango.shelf import SqliteConnector


class SqliteConnectorTestCase(TestCase):

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

    def smoke_test(self, reason='smoke'):
        # Use reason argument for more readable test messages.
        self.assertEquals(self.connector.get('', ''), {})

    def test_db_init(self):
        self.remove_tempfile()
        self.smoke_test('Test non-existent file.')

        self.remove_tempfile()
        open(self.temp_filepath, 'w').close()
        self.smoke_test('Test empty file.')

    def test_get_keymiss(self):
        self.assertEquals(self.connector.get('site', 'rule'), {})

    def test_new_item(self):
        self.assertEquals(self.connector.get('site', 'rule'), {})
        item = {'spam': 'eggs'}
        self.connector.put('site', 'rule', item)
        self.assertEquals(self.connector.get('site', 'rule'), item)

    def test_update_item(self):
        self.test_new_item()
        item = {'spam': 'eggs'}
        update = {'spam': 'eggs', 'foo': 'bar'}
        self.connector.put('site', 'rule', update)
        self.assertEqual(self.connector.get('site', 'rule'), update)
        self.assertNotEqual(self.connector.get('site', 'rule'), item)

    def test_item_separation(self):
        another = {1: 'one', 2: 'two', 3: 'three'}
        yetanother = {4: 'four', 5: 'five', 6: 'six'}
        self.connector.put('site', 'another', another)
        self.test_get_keymiss()
        self.test_new_item()
        self.assertEqual(self.connector.get('site', 'another'), another)
        self.connector.put('yet', 'another', yetanother)
        self.assertEqual(self.connector.get('site', 'another'), another)
        self.assertEqual(self.connector.get('yet', 'another'), yetanother)
        yetanother.update({7: 'seven'})
        self.connector.put('yet', 'another', yetanother)
        self.assertEqual(self.connector.get('site', 'another'), another)


if __name__ == '__main__':
    unittest.main()
