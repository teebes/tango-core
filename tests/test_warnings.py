import unittest
import warnings

from flaskext.testing import TestCase

from tango.app import Tango
from tango.errors import DuplicateContextWarning, DuplicateExportWarning
from tango.errors import DuplicateRouteWarning
from tango.factory import context

import warningsite


class FactoryWarningTestCase(TestCase):

    def create_app(self):
        # For application context setup only.
        return Tango(__name__)

    def setUp(self):
        warnings.simplefilter('always')

    def tearDown(self):
        warnings.simplefilter('ignore')

    def testDuplicateContextWarning(self):
        with warnings.catch_warnings(record=True) as w:
            context.build_package_context(warningsite.content.context)
            assert len(w) == 1
            assert issubclass(w[0].category, DuplicateContextWarning)
            assert 'duplicate context' in str(w[0].message)


    def testDuplicateRouteWarning(self):
        with warnings.catch_warnings(record=True) as w:
            context.build_package_context(warningsite.content.route)
            assert len(w) == 1
            assert issubclass(w[0].category, DuplicateRouteWarning)
            assert 'duplicate route' in str(w[0].message)


    def testDuplicateExportWarning(self):
        with warnings.catch_warnings(record=True) as w:
            context.build_package_context(warningsite.content.export)
            assert len(w) == 1
            assert issubclass(w[0].category, DuplicateExportWarning)
            assert 'duplicate export' in str(w[0].message)


    def testDuplicateMultipleWarnings(self):
        with warnings.catch_warnings(record=True) as w:
            context.build_package_context(warningsite.content)
            assert len(w) == 3


if __name__ == '__main__':
    unittest.main()
