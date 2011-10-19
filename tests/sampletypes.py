"""
site: sampletypes
routes:
 - /
exports:
 - description: Demonstrate various stash types for serialization.
 - a_bool
 - an_empty_dict
 - a_float
 - an_int
 - a_long
 - a_nested_dict
 - a_none
 - a_simple_dict
 - a_simple_list
 - a_simple_tuple
 - a_str
 - a_unicode
"""

a_bool = bool()
an_empty_dict = {}
a_float = 3.141539
an_int = 42
a_long = 123456789012345678901234567890L
a_none = None
a_simple_dict = {'one': 1, 'two': 2, 'three': 3}
a_simple_list = [4, 5, 6]
a_simple_tuple = (7, 8, 9)
a_str = 'Hello, world!'
a_unicode = u'We built that app.\u00ae'
a_nested_dict = {
    'a_bool': a_bool,
    'an_empty_dict': an_empty_dict,
    'a_float': a_float,
    'an_int': an_int,
    'a_long': a_long,
    'a_none': a_none,
    'a_simple_dict': a_simple_dict,
    'a_str': a_str,
    'a_unicode': a_unicode,
    'more_levels': {
        'another_level': {1: 'one', 2: 'two', 'three': 3},
    }
}
