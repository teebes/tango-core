import unittest
import warnings

from flaskext.testing import TestCase

from tango.app import Tango
from tango.errors import DuplicateContextWarning, DuplicateExportWarning
from tango.errors import DuplicateRouteWarning
from tango.factory import context


class FactoryWarningTestCase(TestCase):

    def create_app(self):
        # For application context setup only.
        return Tango(__name__)

    def setUp(self):
        warnings.simplefilter('always')

    def tearDown(self):
        warnings.simplefilter('ignore')

    def test_duplicate_context_warning(self):
        with warnings.catch_warnings(record=True) as w:
            context.build_module_routes('warningsite.stash.context',
                                        import_stash=True)
            assert len(w) == 1
            assert issubclass(w[0].category, DuplicateContextWarning)
            assert 'duplicate context' in str(w[0].message)


    def test_duplicate_route_warning(self):
        with warnings.catch_warnings(record=True) as w:
            context.build_module_routes('warningsite.stash.route')
            assert len(w) == 1
            assert issubclass(w[0].category, DuplicateRouteWarning)
            assert 'duplicate route' in str(w[0].message)


    def test_duplicate_export_warning(self):
        with warnings.catch_warnings(record=True) as w:
            context.build_module_routes('warningsite.stash.export')
            assert len(w) == 1
            assert issubclass(w[0].category, DuplicateExportWarning)
            assert 'duplicate export' in str(w[0].message)


    def test_duplicate_multiple_warnings(self):
        with warnings.catch_warnings(record=True) as w:
            context.build_module_routes('warningsite.stash',
                                        import_stash=True)
            assert len(w) == 3


if __name__ == '__main__':
    unittest.main()
