"Package of utilities for use by Tango sites external to core Tango framework."

import re
import time


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
    >>>
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
    >>>
    """
    value = special_chars_re.sub('', value).strip().lower()
    return dash_and_space_re.sub('-', value)


def make_timestamp(string, formatter):
    """Make a stringified UNIX timestamp out of a given `string` that follows
    the date format specified by `formatter`.

    Dates prior to the UNIX epoch will return a negative result. `string` must
    match the format of `formatter` or a ValueError will be raised.

    Examples:

    >>> make_timestamp('March 04', '%B %y')
    '1078117200'
    >>> make_timestamp('January 1950', '%B %Y')
    '-631134000'
    >>> make_timestamp('Feb.08 2011 4:00 PM', '%b.%d %Y %I:%M %p')
    '1297198800'
    >>> make_timestamp('Feb.08 2011 4:00 PM', '%b.%d %Y %I:%M')
    Traceback (most recent call last):
    ...
    ValueError: unconverted data remains:  PM
    >>>
    """
    struct = time.strptime(string, formatter)
    return format(time.mktime(struct), '.0f')
