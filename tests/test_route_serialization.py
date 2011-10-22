import cPickle as pickle
import pickletools
import unittest

from flaskext.testing import TestCase

from tango.app import Route
from tango.factory.app import build_app


class RouteSerializationTestCase(TestCase):

    def create_app(self):
        return build_app('sampletypes', import_stash=True)

    def setUp(self):
        self.original_route = self.app.routes[0]
        self.serialized = pickle.dumps(self.app.routes)
        self.serialized_optimized = pickletools.optimize(self.serialized)
        self.deserialized = pickle.loads(self.serialized)
        self.deserialized_optimized = pickle.loads(self.serialized_optimized)

    def tearDown(self):
        pass

    def _test_deserialization_type(self, deserialized):
        self.assertEqual(len(deserialized), 1)
        route = deserialized[0]
        self.assertEqual(type(route), Route)

    def test_deserialization_type(self):
        self._test_deserialization_type(self.deserialized)

    def test_deserialization_type_optimized(self):
        self._test_deserialization_type(self.deserialized_optimized)

    def _test_route_attributes(self, deserialized):
        route = deserialized[0]
        original_route = self.original_route
        self.assertEqual(route.site, original_route.site)
        self.assertEqual(route.rule, original_route.rule)
        self.assertEqual(route.exports, original_route.exports)
        self.assertEqual(route.static, original_route.static)
        self.assertEqual(route.writer_name, original_route.writer_name)
        # Unable to test context by simple equivalence.
        self.assertEqual(route.modules, original_route.modules)

    def test_route_attributes(self):
        self._test_route_attributes(self.deserialized)

    def test_route_attributes_optimized(self):
        self._test_route_attributes(self.deserialized_optimized)

    def compare_scalars_in_dict(self, dict1, dict2):
        for key in ('a_bool', 'an_empty_dict', 'a_float', 'an_int', 'a_long',
                    'a_none', 'a_simple_dict', 'a_str', 'a_unicode'):
            self.assertEqual(dict1[key], dict2[key])

    def _test_stash_scalar_types(self, deserialized):
        context = deserialized[0].context
        context_original = self.original_route.context
        self.compare_scalars_in_dict(context, context_original)

    def test_stash_scalar_types(self):
        self._test_stash_scalar_types(self.deserialized)

    def test_stash_scalar_types_optimized(self):
        self._test_stash_scalar_types(self.deserialized_optimized)

    def _test_stash_iterables(self, deserialized):
        context = deserialized[0].context
        context_original = self.original_route.context
        for key in ('a_simple_list', 'a_simple_tuple'):
            self.assertEqual(context[key], context_original[key])

    def test_stash_iterables(self):
        self._test_stash_iterables(self.deserialized)

    def test_stash_iterables_optimized(self):
        self._test_stash_iterables(self.deserialized_optimized)

    def _test_stash_nested_dict(self, deserialized):
        a_nested_dict = deserialized[0].context['a_nested_dict']
        a_nested_dict_original = self.original_route.context['a_nested_dict']
        self.compare_scalars_in_dict(a_nested_dict, a_nested_dict_original)

        more_levels = a_nested_dict['more_levels']
        more_levels_original = a_nested_dict_original['more_levels']

        another_level = more_levels['another_level']
        another_level_original = more_levels_original['another_level']
        self.assertEqual(another_level, another_level_original)

    def test_stash_nested_dict(self):
        self._test_stash_nested_dict(self.deserialized)

    def test_stash_nested_dict_optimized(self):
        self._test_stash_nested_dict(self.deserialized_optimized)


if __name__ == '__main__':
    unittest.main()
