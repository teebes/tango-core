"Tools for generating context content from existing (X)HTML documents."

import urllib2

from lxml import etree
from lxml.cssselect import CSSSelector


parser = etree.HTMLParser()


def dict_zip(**kwargs):
    """Return a list of dictionaries from provided iterable keyword arguments.

    Each dictionary returned contains one value, in order, from each provided
    iterable. The key for each value is taken from the key of the iterable from
    which it originated. If the provided iterables are of different lengths, the
    list of dictionaries will have a length equal to the shortest iterable.

    Examples:
    >>> meals = ('breakfast', 'dinner')
    >>> foods = ('spam', 'eggs')
    >>> dict_zip(meal=meals, food=foods)
    [{'food': 'spam', 'meal': 'breakfast'}, {'food': 'eggs', 'meal': 'dinner'}]
    >>> names = ('oilman',)
    >>> roles = ('worker', 'empty')
    >>> dict_zip(name=names, role=roles)
    [{'role': 'worker', 'name': 'oilman'}]

    """
    return [dict(zip(kwargs.keys(), item)) for item in zip(*kwargs.values())]


def url_selector(url, selector, text_only=False):
    """Return the unicode representation of an HTML element from `url` matched
    by `selector`.

    If `selector` matches multiple elements, they will be concatenated into a
    single unicode string.

    Straightforward case:
    >>> url_selector(my_url, 'h1').strip()
    u'<h1>This is just for testing.</h1>'
    >>> url_selector(my_url, 'h1', text_only=True)
    u'This is just for testing.'

    Grabbing HTML snippets:
    >>> print url_selector(my_url, 'ul')
    <ul><li>Item 1</li>
      <li>Item 2</li>
      <li>Item 3</li>
    </ul>
    >>> print url_selector(my_url, 'li')
    <li>Item 1</li>
      <li>Item 2</li>
      <li>Item 3</li>
    <BLANKLINE>
    >>> url_selector(my_url, 'li', True)
    u'Item 1Item 2Item 3'
    >>>
    """
    tree = etree.parse(urllib2.urlopen(url), parser)
    cs = CSSSelector(selector)
    source = u''
    for branch in cs(tree):
        if text_only:
            source += branch.text
        else:
            source += etree.tostring(branch)
    return source


def url_selector_list(url, selector, text_only=False):
    """Return a list of HTML elements from `url` matched by `selector`, converted
    to unicode strings.

    If `text_only` is True, only the text contents of the matched elements are
    included.

    Common use:
    >>> url_selector_list(my_url, 'li', True)
    ['Item 1', 'Item 2', 'Item 3']
    >>> url_selector_list(my_url, 'span a') # doctest:+NORMALIZE_WHITESPACE
    ['<a href="a.html">Link A</a>',
     '<a href="b.html">Link B</a>',
     '<a href="c.html">Link C</a>']
    >>> url_selector_list(my_url, 'span a', True)
    ['Link A', 'Link B', 'Link C']

    More examples:
    >>> [result.strip() for result in url_selector_list(my_url, 'li')]
    ['<li>Item 1</li>', '<li>Item 2</li>', '<li>Item 3</li>']
    >>> url_selector_list(my_url, 'h1', True)
    ['This is just for testing.']
    >>> [result.strip() for result in url_selector_list(my_url, 'h1')]
    ['<h1>This is just for testing.</h1>']
    >>>
    """
    tree = etree.parse(urllib2.urlopen(url), parser)
    cs = CSSSelector(selector)
    if text_only:
        return [branch.text for branch in cs(tree)]
    return [etree.tostring(branch) for branch in cs(tree)]


# For testing:

import os.path

directory = os.path.dirname(os.path.abspath(__file__))
tests_directory = os.path.abspath(os.path.join(directory, '../../tests/'))
my_url = 'file://' + tests_directory + '/simple.html'
