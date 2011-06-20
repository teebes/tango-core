import filecmp
import os
import shutil
import tempfile
import unittest

from flaskext.testing import TestCase

from tango.build import build_static_site
from tango.factory import build_app


class AppInitTestCase(TestCase):

    def create_app(self):
        output = tempfile.mkdtemp()
        options = {
            'output': output,
            'force_overwrite': True,
            }
        app = build_app('testsite')
        return build_static_site(app, **options)

    def setUp(self):
        pass

    def tearDown(self):
        shutil.rmtree(self.app.config['TANGO_BUILD_DIR'])

    def test_consistent_build(self):
        # TODO: Add recursive directory testing.
        orig = os.path.dirname(os.path.abspath(__file__)) + '/testsite-build'
        dest = self.app.config['TANGO_BUILD_DIR']
        diff = filecmp.dircmp(orig, dest)
        self.assertEqual(diff.left_only, [])
        self.assertEqual(diff.right_only, [])
        self.assertEqual(diff.diff_files, [])


if __name__ == '__main__':
    unittest.main()
