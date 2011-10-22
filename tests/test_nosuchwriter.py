import unittest

from tango.errors import NoSuchWriterException
from tango.factory.app import build_app


class NoSuchWriterTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_no_such_writer_exception(self):
        self.assertRaises(NoSuchWriterException, build_app, 'nosuchwriter')


if __name__ == '__main__':
    unittest.main()
