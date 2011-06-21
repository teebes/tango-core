import filecmp
import os
import shutil
import tempfile
import unittest

from flaskext.testing import TestCase

from tango.build import build_static_site
from tango.factory import build_app


class BuildTestsiteTestCase(TestCase):

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

    def assert_no_diffs_in_dircmp(self, dircmp_obj):
        self.assertEqual(dircmp_obj.left_only, [])
        self.assertEqual(dircmp_obj.right_only, [])
        self.assertEqual(dircmp_obj.diff_files, [])
        for subdircmp_obj in dircmp_obj.subdirs.itervalues():
            self.assert_no_diffs_in_dircmp(subdircmp_obj)


    def test_consistent_build(self):
        orig = os.path.dirname(os.path.abspath(__file__)) + '/testsite-build'
        dest = self.app.config['TANGO_BUILD_DIR']
        dircmp_obj = filecmp.dircmp(orig, dest)
        self.assert_no_diffs_in_dircmp(dircmp_obj)


if __name__ == '__main__':
    unittest.main()
