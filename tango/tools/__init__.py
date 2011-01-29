"Package of utilities for use by Tango sites external to core Tango framework."

import re


first_cap_re = re.compile('(.)([A-Z][a-z]+)')
all_cap_re = re.compile('([a-z0-9])([A-Z])')


def camel_case(name):
    """Convert CamelCase to style of camel_case. StackOverflow #1175208

    Examples:

    >>> camel_case('camel')
    'camel'
    >>> camel_case('Camel')
    'camel'
    >>> camel_case('CamelCase')
    'camel_case'
    >>> camel_case('camelCase')
    'camel_case'
    >>> camel_case('CamelCamelCase')
    'camel_camel_case'
    >>> camel_case('Camel2Camel2Case')
    'camel2_camel2_case'
    >>> camel_case('getHTTPResponseCode')
    'get_http_response_code'
    >>> camel_case('get2HTTPResponseCode')
    'get2_http_response_code'
    >>> camel_case('HTTPResponseCode')
    'http_response_code'
    >>> camel_case('HTTPResponseCodeXYZ')
    'http_response_code_xyz'

    """
    first_pass = first_cap_re.sub(r'\1_\2', name)
    return all_cap_re.sub(r'\1_\2', first_pass).lower()


special_chars_re = re.compile('[^\w\s-]')
dash_and_space_re = re.compile('[-\s]+')


def slugify(value):
    """Normalize a string to a url-ready slug by lowercasing, converting spaces
    to hyphens, and removing non-alpha characters.

    Examples:

    >>> slugify('slug')
    'slug'
    >>> slugify('a slug')
    'a-slug'
    >>> slugify('  a slug')
    'a-slug'
    >>> slugify('&%a@-*slug')
    'a-slug'
    >>> slugify('crAZy CaPs')
    'crazy-caps'
    >>> slugify('a - slug')
    'a-slug'
    >>> slugify('-a slug')
    '-a-slug'


    """
    value = special_chars_re.sub('', value).strip().lower()
    return dash_and_space_re.sub('-', value)
