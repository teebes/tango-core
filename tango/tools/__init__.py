"Package of utilities for use by Tango sites external to core Tango framework."

import csv
import re
from datetime import date
from time import mktime, strptime


first_cap_re = re.compile('(.)([A-Z][a-z]+)')
all_cap_re = re.compile('([a-z0-9])([A-Z])')


def simple_text_to_html(content):
    """
    Puts <p> around lines of text, creates <ul> / <li> for lines that begin
    with *

    >>> text = "Simple line of text."
    >>> print(simple_text_to_html(text))
    <p>Simple line of text.</p>
    <BLANKLINE>
    >>>

    >>> text = '''Simple line of text.
    ...
    ... And another line.'''
    >>> print(simple_text_to_html(text))
    <p>Simple line of text.</p>
    <p>And another line.</p>
    <BLANKLINE>
    >>>

    >>> text = '''Simple line of text followed by a list:
    ...
    ... * with an item
    ... * and another item'''
    >>> print(simple_text_to_html(text))
    <p>Simple line of text followed by a list:</p>
    <ul>
    <li>with an item</li>
    <li>and another item</li>
    </ul>
    <BLANKLINE>
    >>>

    >>> text = '''
    ...
    ...
    ...
    ...
    ... '''
    >>> print(simple_text_to_html(text))
    <BLANKLINE>
    >>>

    >>> text = '''A paragraph followed by a list:
    ... * item A
    ... * item B
    ... Followed by another paragraph and then two lists:
    ... * item alpha
    ... * item beta
    ...
    ... * item gamma
    ... * item delta'''
    >>> print(simple_text_to_html(text))
    <p>A paragraph followed by a list:</p>
    <ul>
    <li>item A</li>
    <li>item B</li>
    </ul>
    <p>Followed by another paragraph and then two lists:</p>
    <ul>
    <li>item alpha</li>
    <li>item beta</li>
    </ul>
    <ul>
    <li>item gamma</li>
    <li>item delta</li>
    </ul>
    <BLANKLINE>
    >>>
    """

    current_tag = None
    output = ""

    for line in content.split('\n'):
        # strip precending empty characters
        re.sub('^\s', '', line)

        if not line:
            # Ignore empty lines, but if in a list, close the list.
            if current_tag == 'ul':
                output += "</ul>\n"
                current_tag = None
        else:
            # * lines are list items, create list if necessary
            if line[0] == '*':
                if current_tag != 'ul':
                    output += "<ul>\n"
                    current_tag = 'ul'
                output += "<li>%s</li>\n" % line[2:]
            # everything else, for now, is a paragraph
            else:
                if current_tag == 'ul':
                    output += '</ul>\n'
                    current_tag = None
                output += '<p>%s</p>\n' % line

    # if we're done with the content but still have an open list, close it
    if current_tag == 'ul':
        output += '</ul>\n'

    return output

def UnicodeDictReader(utf8_data, **kwargs):
    """A (mostly) UTF8-safe wrapper for csv.DictReader.

    This function does not encode the header row, and there's likely a less
    fragile way to skin the proverbial cat. See: http://bit.ly/gR6qnN

    >>> contents = [i for i in UnicodeDictReader(open(csv_test_file, 'rU'))]
    >>> contents[0]['colA']
    u'row1A'
    >>> contents[0]['colB']
    u'row1B'
    >>> contents[1]['colA']
    u'row2A'
    >>> contents[1]['colB']
    u'row2B'

    """
    reader = csv.DictReader(utf8_data, **kwargs)
    for row in reader:
        yield dict([(key, unicode(value, 'utf-8'))
                    for key, value in row.iteritems()])


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
    """Make a stringified UNIX timestamp out of a given ``string`` that follows
    the date format specified by ``formatter``.

    Dates prior to the UNIX epoch will return a negative result. ``string``
    must match the format of ``formatter`` or a ValueError will be raised.

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
    struct = strptime(string, formatter)
    return format(mktime(struct), '.0f')


def date_from_string(string, formatter):
    """Return a datetime date object from a given ``string`` that follows the
    date format specified by ``formatter``.

    At minimum, the function requires that ``formatter`` contain a day and a
    month.  When year is not given, date defaults to current year.

    Raises Value error when ``string`` does not match ``formatter``.

    Examples:

    >>> date_from_string('November 11, 2011', '%B %d, %Y')
    datetime.date(2011, 11, 11)
    >>> date_from_string('November 11', '%B %d') #doctest:+ELLIPSIS
    datetime.date(..., 11, 11)
    >>> _.year == date.today().year
    True
    >>> date_from_string('Feb.08 4:00 PM', '%b.%d %I:%M %p') #doctest:+ELLIPSIS
    datetime.date(..., 2, 8)
    >>> _.year == date.today().year
    True
    >>> date_from_string('Feb.08 2011 4:00 PM', '%b.%d %Y %I:%M %p')
    datetime.date(2011, 2, 8)
    >>> date_from_string('Feb.08 2011 4:00 PM', '%b.%d %Y %I:%M')
    Traceback (most recent call last):
    ...
    ValueError: unconverted data remains:  PM
    >>>
    """
    struct = strptime(string, formatter)
    if ('%Y' not in formatter and
        '%y' not in formatter and
        struct.tm_year == 1900):
        return date(date.today().year, struct.tm_mon, struct.tm_mday)
    return date.fromtimestamp(mktime(struct))


def url_parameter_match(route, parameter):
    """Determine whether a route contains a url parameter, return True if so.

    Example:
    >>> url_parameter_match('/<argument>', 'argument')
    True
    >>> url_parameter_match('/<argument>/', 'argument')
    True
    >>> url_parameter_match('/<int:argument>', 'argument')
    True
    >>> url_parameter_match('/int:<argument>/', 'argument')
    True
    >>> url_parameter_match('/path:<argument>/', 'argument')
    True
    >>> url_parameter_match('/path/to/<parameter>/', 'parameter')
    True
    >>> url_parameter_match('/path/to/<path:parameter>/', 'parameter')
    True
    >>> url_parameter_match('/path/to/<aparameter>/', 'parameter')
    False
    >>> url_parameter_match('/path/to/<path:aparameter>/', 'parameter')
    False
    >>> url_parameter_match('/', 'parameter')
    False
    >>>
    """
    return re.search('[<:]{0}>'.format(parameter), route) is not None


# For testing:
import os.path

directory = os.path.dirname(os.path.abspath(__file__))
tests_directory = os.path.abspath(os.path.join(directory, '../../tests/'))
csv_test_file = tests_directory + '/csv.csv' # for the UnicodeDictReader test
