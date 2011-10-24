import unittest

from tango.factory.app import get_app


class SingleModuleAppTestCase(unittest.TestCase):

    def test_get_app(self):
        # Tango avoids import side-effects when instantiating applications.
        # For packages, this is generally not a problem, where __init__.py is
        # often empty (yet __init__ must be imported when discovering modules).
        #
        # As a test, build an application from a module with valid metadata,
        # which raises an error at runtime.
        get_app('importerror') # must load single-module apps without import
        # Test passes if get_app('importerror') did not error out.

        # A note on testing style:
        # This test could try/except, and self.fail('...') on ImportError.
        # But then a developer does not get meaningful tracebacks.


if __name__ == '__main__':
    unittest.main()
