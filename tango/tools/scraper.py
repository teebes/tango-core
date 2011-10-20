"Tools for generating context from existing (X)HTML documents."

import urllib2
from urllib import quote

from lxml import etree
from lxml.cssselect import CSSSelector
# TODO: Factor out BeautifulSoup, replace with lxml.
from BeautifulSoup import BeautifulSoup, NavigableString

from tango.errors import ParseError

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
    >>>
    """
    return [dict(zip(kwargs.keys(), item)) for item in zip(*kwargs.values())]


# TODO: These functions should be replaced by a single-fetch DOM-based object
# (lazy fetch on first time needed) which provides selector methods which can
# be used multiple times against the same string data returned by the URL
# (fetched once).


def get_with_selector(content, selector, text_only=False, content_type='string',
                      parser='HTMLParser'):
    """Provide unicode of element `content` matched by `selector`.

    If `selector` matches multiple elements, they will be concatenated into a
    single unicode string. If text_only is true, only the contents of the
    matched element will be returned.  If content_type is 'url', content will
    be treated as a URL and its contents will be loaded and processed with with
    the selector.

    >>> get_with_selector("<b>I am bold.</b>", 'b')
    u'<b>I am bold.</b>'
    >>> get_with_selector("<b>I am bold.</b>", 'b', True)
    u'I am bold.'
    >>> get_with_selector("<b></b>", 'b')
    u'<b/>'
    >>> get_with_selector("<b></b>", 'b', True)
    >>> get_with_selector("<b/>", 'b')
    u'<b/>'
    >>>

    Provide a content_type of 'string' or 'url'.  The example above uses a
    string.  When given a URL as content, and 'url' as the content_type, this
    function opens the URL to get the content.

    >>> get_with_selector(my_url, 'h1', content_type='url').strip()
    u'<h1>This is just for testing.</h1>'
    >>> get_with_selector("<b>I am bold.</b>", 'b', content_type='spam')
    Traceback (most recent call last):
        ...
    ParseError: Invalid content type 'spam'
    >>>

    Expect unexpected return values or empty strings when content is a URL but
    content_type is not set to 'url'.  This API is built for convenience.

    >>> get_with_selector(my_url, 'h1')
    u''
    >>>

    Provide a parser in the lxml.etree namespace.
    See http://lxml.de/api/index.html for a full reference.
    >>> get_with_selector("<b>I am bold.</b>", 'b', parser='NotAParser')
    Traceback (most recent call last):
        ...
    ParseError: Invalid parser 'NotAParser'
    >>>
    """
    try:
        loaded_parser = getattr(etree, parser)()
    except AttributeError:
        raise ParseError("Invalid parser '%s'" % parser)

    if content_type == 'string':
        tree = etree.fromstring(content, loaded_parser)
    elif content_type == 'url':
        tree = etree.parse(urllib2.urlopen(content), loaded_parser)
    else:
        raise ParseError("Invalid content type '%s'" % content_type)

    cs = CSSSelector(selector)
    output = u''
    for branch in cs(tree):
        if text_only:
            try:
                output += branch.text
            except TypeError:
                # branch.text is empty
                output = None
        else:
            output += etree.tostring(branch)
    return output


def url_selector(url, selector, text_only=False):
    """Provide unicode of HTML element from `url` matched by `selector`.

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
    """Provide unicode of HTML elements from `url` matched by `selector`.

    If `text_only` is True, only the text contents of the matched elements are
    included.

    Common use:
    >>> url_selector_list(my_url, 'li', True)
    ['Item 1', 'Item 2', 'Item 3']
    >>> url_selector_list(my_url, 'span a') # doctest:+NORMALIZE_WHITESPACE
    ['<a href="a.html">Link A</a>',
     '<a href="b.html">Link B</a>',
     '<a href="c.html" rel="external">Link C</a>']
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


def url_selector_values(url, selector, attr):
    """Provide attribute list of type `attr` from `selector` match at `url`.

    If an attribute is not present for a matched element, `None` is added to the
    returned list.

    Common use:
    >>> url_selector_values(my_url, 'span a', 'href')
    ['a.html', 'b.html', 'c.html']
    >>> url_selector_values(my_url, 'span a', 'rel')
    [None, None, 'external']
    >>> url_selector_values(my_url, 'span a', 'foo')
    [None, None, None]
    >>>
    """
    tree = etree.parse(urllib2.urlopen(url), parser)
    cs = CSSSelector(selector)
    return [branch.get(attr) for branch in cs(tree)]


def strip_tags(tags, html):
    """Remove each tag type specified in list `tags` from a chunk of html.

    If providing only one tag, `tags` may be a string. Only tags are stripped
    from the html chunk; tag contents are left untouched.

    Common use:
    >>> html = '<span>This is <a href="a.html">Link <br />A</a></span>'
    >>> strip_tags('a', html)
    '<span>This is Link <br />A</span>'
    >>> strip_tags(['a', 'br'], html)
    '<span>This is Link A</span>'
    >>> strip_tags(['span', 'a', 'br'], html)
    'This is Link A'
    >>>
    """
    soup = BeautifulSoup(html)
    for tag in soup.findAll(True):
        if tag.name in tags:
            s = ""
            for c in tag.contents:
                if type(c) != NavigableString:
                    c = strip_tags(tags, unicode(c))
                s += unicode(c)
            tag.replaceWith(s)
    return str(soup)


def escape_links(html):
    """Escape unsafe characters in all href/src paths in `html`.

    This is primarily useful for spaces and parentheses.

    Examples:
    >>> html = '<a href="/emily connolly/">Emily Connolly</a>'
    >>> escape_links(html)
    '<a href="/emily%20connolly/">Emily Connolly</a>'
    >>> html2 = '<img src="spaces (and parens).jpg" alt="" />'
    >>> escape_links(html2)
    '<img src="spaces%20%28and%20parens%29.jpg" alt="" />'
    >>>
    """
    soup = BeautifulSoup(html)
    safe_chars = "%/:=&?~#+!$,;'@*[]"
    for tag in soup.findAll(True):
        if tag.has_key('href'):
            tag['href'] = quote(tag['href'], safe=safe_chars)
        elif tag.has_key('src'):
            tag['src'] = quote(tag['src'], safe=safe_chars)
    return str(soup)


def remove_attributes(tags, attrs, html):
    """Remove attributes `attrs` from elements in `tags` contained in `html`.

    If providing only one tag, `tags` may be a string.

    Common use:
    >>> html = '<div class="spam"><span class="eggs">Text</span></div>'
    >>> remove_attributes('span', ['class'], html)
    '<div class="spam"><span>Text</span></div>'
    >>> remove_attributes(['div', 'span'], ['class'], html)
    '<div><span>Text</span></div>'
    >>> html2 = '<img src="#" alt="An alt value" id="spam" />'
    >>> remove_attributes('img', ['alt', 'id'], html2)
    '<img src="#" />'
    >>>
    """
    soup = BeautifulSoup(html)
    for tag in soup.findAll(True):
        if tag.name in tags:
            for attr in attrs:
                if tag.has_key(attr):
                    del(tag[attr])
    return str(soup)


def remove_elements(tags, html, attrs={}):
    """Remove all elements from `html` specfied in a list `tags`.

    If providing only one tag, `tags` may be a string. If an `attrs` dictionary
    is provided, only elements with attribute values specified will be removed.
    The `attrs` dictionary should contain attribute names as keys. Values can be
    strings or regular expressions.

    Note: a named `attrs` dictionary instead of `kwargs` to avoid conflicts with
    Python's `class` statement when selecting by CSS class.

    Common use:
    >>> html = '<span>This is <a href="a.html">Link <br />A</a></span>'
    >>> remove_elements('a', html)
    '<span>This is </span>'
    >>> html2 = 'An image<img class="spam" src="#" alt="" />'
    >>> remove_elements('img', html2, attrs={'class': 'spam'})
    'An image'
    >>> remove_elements('img', html2, attrs={'class': 'foo'})
    'An image<img class="spam" src="#" alt="" />'
    >>>
    """
    soup = BeautifulSoup(html)
    for tag in soup.findAll(attrs=attrs):
        if tag.name in tags:
            tag.replaceWith('')
    return str(soup)


# For testing:

import os.path

directory = os.path.dirname(os.path.abspath(__file__))
tests_directory = os.path.abspath(os.path.join(directory, '../../tests/'))
my_url = 'file://' + tests_directory + '/simple.html'
