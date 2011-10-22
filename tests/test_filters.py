import datetime
import unittest

from flaskext.testing import TestCase

from tango.factory.app import build_app
from tango import filters


class FiltersTestCase(TestCase):

    def create_app(self):
        return build_app('simplesite')

    def setUp(self):
        self.client = self.app.test_client()

    def tearDown(self):
        pass

    def test_datetime(self):
        dt = datetime.datetime(2010, 3, 12, 12, 34, 56)

        raw_datetime = filters.datetime
        assert 'datetime' in self.app.jinja_env.filters.keys()
        app_datetime = self.app.jinja_env.filters['datetime']

        self.assertEqual(raw_datetime(dt), '2010-03-12 12:34:56')
        self.assertEqual(app_datetime(dt), '2010-03-12 12:34:56')

        self.assertEqual(raw_datetime(dt, '%m/%d/%Y'), '03/12/2010')
        self.assertEqual(app_datetime(dt, '%m/%d/%Y'), '03/12/2010')

        self.app.config['DEFAULT_DATETIME_FORMAT'] = '%m/%d/%y'

        self.assertEqual(raw_datetime(dt), '03/12/10')
        self.assertEqual(app_datetime(dt), '03/12/10')
        self.assertEqual(raw_datetime(dt, None), '2010-03-12 12:34:56')
        self.assertEqual(app_datetime(dt, None), '2010-03-12 12:34:56')
        self.assertEqual(raw_datetime(dt, format=None), '2010-03-12 12:34:56')
        self.assertEqual(app_datetime(dt, format=None), '2010-03-12 12:34:56')

        # Test for correct use of default date vs datetime.
        self.app.config['DEFAULT_DATE_FORMAT'] = 'You should not see me.'
        self.app.config['DEFAULT_DATETIME_FORMAT'] = None

        self.assertEqual(raw_datetime(dt), '2010-03-12 12:34:56')
        self.assertEqual(app_datetime(dt), '2010-03-12 12:34:56')

    def test_date(self):
        d = datetime.date(2010, 3, 12)

        raw_date = filters.date
        assert 'date' in self.app.jinja_env.filters.keys()
        app_date = self.app.jinja_env.filters['date']

        self.assertEqual(raw_date(d), '2010-03-12')
        self.assertEqual(app_date(d), '2010-03-12')

        self.assertEqual(raw_date(d, '%m/%d/%Y'), '03/12/2010')
        self.assertEqual(app_date(d, '%m/%d/%Y'), '03/12/2010')

        self.app.config['DEFAULT_DATE_FORMAT'] = '%m/%d/%y'

        self.assertEqual(raw_date(d), '03/12/10')
        self.assertEqual(app_date(d), '03/12/10')
        self.assertEqual(raw_date(d, None), '2010-03-12')
        self.assertEqual(app_date(d, None), '2010-03-12')
        self.assertEqual(raw_date(d, format=None), '2010-03-12')
        self.assertEqual(app_date(d, format=None), '2010-03-12')

        # Test for correct use of default date vs datetime.
        self.app.config['DEFAULT_DATE_FORMAT'] = None
        self.app.config['DEFAULT_DATETIME_FORMAT'] = 'You should not see me.'

        self.assertEqual(raw_date(d), '2010-03-12')
        self.assertEqual(app_date(d), '2010-03-12')

    def test_struct_time(self):
        st = datetime.datetime(2010, 3, 12, 12, 34, 56).timetuple()

        raw_struct_time = filters.struct_time
        assert 'struct_time' in self.app.jinja_env.filters.keys()
        app_struct_time = self.app.jinja_env.filters['struct_time']

        self.assertEqual(raw_struct_time(st), '2010-03-12 12:34:56')
        self.assertEqual(app_struct_time(st), '2010-03-12 12:34:56')

        self.assertEqual(raw_struct_time(st, '%m/%d/%Y'), '03/12/2010')
        self.assertEqual(app_struct_time(st, '%m/%d/%Y'), '03/12/2010')

        self.app.config['DEFAULT_DATETIME_FORMAT'] = '%m/%d/%y'

        self.assertEqual(raw_struct_time(st), '03/12/10')
        self.assertEqual(app_struct_time(st), '03/12/10')
        self.assertEqual(raw_struct_time(st, None), '2010-03-12 12:34:56')
        self.assertEqual(app_struct_time(st, None), '2010-03-12 12:34:56')
        self.assertEqual(raw_struct_time(st, format=None), '2010-03-12 12:34:56')
        self.assertEqual(app_struct_time(st, format=None), '2010-03-12 12:34:56')

        self.app.config['DEFAULT_DATETIME_FORMAT'] = None

        self.assertEqual(raw_struct_time(st), '2010-03-12 12:34:56')
        self.assertEqual(app_struct_time(st), '2010-03-12 12:34:56')


if __name__ == '__main__':
    unittest.main()
