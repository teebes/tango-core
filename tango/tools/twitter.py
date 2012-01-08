"Tools for interacting with the Twitter API and parsing tweets."

import re
from urllib import urlencode

import oauth2 as oauth


class TwitterAPICallFailed(Exception):
    "Error when calling twitter API."


def parse_link(text):
    """Parse a tweet and add a link tag where text is a link.

    Example:
    >>> parse_link('A link to http://battle.net')
    "A link to <a href='http://battle.net'>http://battle.net</a>"
    >>>
    """
    return re.sub(
        r"(http(s)?://[\w./?=%&amp;\-]+)",
        lambda x: "<a href='%s'>%s</a>" % (x.group(), x.group()),
        text
    )


def parse_at(text):
    """Parse a tweet and add links for @mentions.

    Example:
    >>> parse_at('A reference to @teebesz')
    "A reference to <a href='http://twitter.com/teebesz'>@teebesz</a>"
    >>>
    """
    return re.sub(
        r'@(\w+)',
        lambda x: "<a href='http://twitter.com/%s'>%s</a>" \
            % (x.group()[1:], x.group()),
        text
    )


def parse_hashtag(text):
    """Parse a tweet and add links for each #hashtag.

    Example:
    >>> parse_hashtag('A twitter #hashtag')
    "A twitter <a href='http://twitter.com/search?q=%23hashtag'>#hashtag</a>"
    >>>
    """
    return re.sub(
        r'#(\w+)',
        lambda x: "<a href='http://twitter.com/search?q=%%23%s'>%s</a>" \
            % (x.group()[1:], x.group()),
        text
    )


class TwitterAPI(object):
    "Simple API wrapper for api.twitter.com using oauth."

    BASE_URI = 'https://api.twitter.com/1'

    def __init__(self, **kwargs):
        self.consumer_secret = kwargs.get('CONSUMER_SECRET', '')
        self.consumer_key = kwargs.get('CONSUMER_KEY', '')
        self.oauth_token = kwargs.get('OAUTH_TOKEN', '')
        self.oauth_token_secret = kwargs.get('OAUTH_TOKEN_SECRET', '')

    def __call__(self, url, method='GET', params=None):
        token = oauth.Token(key=self.oauth_token,
                            secret=self.oauth_token_secret)
        consumer = oauth.Consumer(key=self.consumer_key,
                                  secret=self.consumer_secret)
        client = oauth.Client(consumer, token)

        if url[0] != '/':
            url = '/' + url
        url = "%s%s" % (self.BASE_URI, url)

        if params:
            if method == 'GET':
                url += "?" + urlencode(params)
                resp, content = client.request(url, method)
            elif method in ('POST', 'PUT'):
                resp, content = client.request(url, method, urlencode(params))
        else:
            resp, content = client.request(url, method)

        if int(resp.get('status', 0)) != 200:
            raise TwitterAPICallFailed(resp, content)

        return resp, content


def _test():
    """Test the Twitter API wrapper by verifying it's oauth client calls.

    Mock the OAuth client used by TwitterAPI.
    >>> from minimock import Mock, restore
    >>> mock_client = Mock('oauth_client')
    >>> oauth.Client = Mock('oauth.Client')
    >>> oauth.Client.mock_returns = mock_client
    >>> mock_request = Mock('oauth.Client.request')
    >>> mock_client.request = mock_request
    >>> mock_request.mock_returns = {'status': 200}, 'Hello!'
    >>>

    Create a twitter API client as an instance of the TwitterAPI wrapper.
    >>> twitter = TwitterAPI(
    ...     CONSUMER_SECRET='MY_CONSUMER_SECRET',
    ...     CONSUMER_KEY='MY_CONSUMER_KEY',
    ...     OAUTH_TOKEN='MY_OAUTH_TOKEN',
    ...     OAUTH_TOKEN_SECRET='MY_OAUTH_TOKEN_SECRET',
    ... )
    ...
    >>>

    Now test TwitterAPI for how it marshals calls through the OAuth client.
    Test the simplest call.
    >>> twitter('/') # doctest:+ELLIPSIS
    Called oauth.Client(
        <oauth2.Consumer object at 0x...>,
        <oauth2.Token object at 0x...>)
    Called oauth.Client.request('https://api.twitter.com/1/', 'GET')
    ({'status': 200}, 'Hello!')
    >>>

    Test for how the wrapper handles no slash in front.
    >>> twitter('no-slash-in-front') # doctest:+ELLIPSIS
    Called oauth.Client(
        <oauth2.Consumer object at 0x...>,
        <oauth2.Token object at 0x...>)
    Called oauth.Client.request(
        'https://api.twitter.com/1/no-slash-in-front',
        'GET')
    ({'status': 200}, 'Hello!')
    >>>

    Test GET calls with parameters.
    >>> twitter('/foo', params={'q': 'spam'}) # doctest:+ELLIPSIS
    Called oauth.Client(
        <oauth2.Consumer object at 0x...>,
        <oauth2.Token object at 0x...>)
    Called oauth.Client.request('https://api.twitter.com/1/foo?q=spam', 'GET')
    ({'status': 200}, 'Hello!')
    >>> twitter('/foo', params={'q': 'spam', 'hl': 'en'})
    ... # doctest:+ELLIPSIS,+NORMALIZE_WHITESPACE
    Called oauth.Client(
        <oauth2.Consumer object at 0x...>,
        <oauth2.Token object at 0x...>)
    Called oauth.Client.request('https://api.twitter.com/1/foo?q=spam&hl=en',
        'GET')
    ({'status': 200}, 'Hello!')

    Test POST calls.
    >>> twitter('/foo', method='POST') # doctest:+ELLIPSIS
    Called oauth.Client(
        <oauth2.Consumer object at 0x...>,
        <oauth2.Token object at 0x...>)
    Called oauth.Client.request('https://api.twitter.com/1/foo', 'POST')
    ({'status': 200}, 'Hello!')
    >>> twitter('/foo', method='POST', params={'q': 'spam', 'hl': 'en'})
    ... # doctest:+ELLIPSIS
    Called oauth.Client(
        <oauth2.Consumer object at 0x...>,
        <oauth2.Token object at 0x...>)
    Called oauth.Client.request(
        'https://api.twitter.com/1/foo',
        'POST',
        'q=spam&hl=en')
    ({'status': 200}, 'Hello!')
    >>>

    Test a non-200 HTTP OK response.
    >>> mock_request.mock_returns = {'status': 404}, 'Not Found'
    >>> twitter('/nutrition-in-fast-food-hamburger') # doctest:+ELLIPSIS
    Traceback (most recent call last):
        ...
    TwitterAPICallFailed: ({'status': 404}, 'Not Found')
    >>>

    Restore mocked objects to their originals.
    >>> restore()
    >>>
    """
