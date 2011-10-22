"Response writers, which take a template context and return a string."

import json
import mimetypes
import types

from flask import render_template


class BaseWriter(object):
    """A response writer, given a template context.

    Initialize an instance of a BaseWriter subclass, then call it.

        writer = Writer()
        writer(template_context)

    Any callable can be a writer, accepting a template context as its argument.

        a_callable(template_context)

    Set mimetype attribute as appropriate or to None to use app's default,
    i.e. app.response_class.default_mimetype.

    A subclass must implement a write method:
    >>> class IncompleteWriter(BaseWriter):
    ...     "Does not implement the write method."
    ...
    >>> incomplete = IncompleteWriter()
    >>> incomplete(test_context)
    Traceback (most recent call last):
       ...
    NotImplementedError: Where is this writer's write method?
    >>>
    """

    # mimetype/Content-Type to use in the HTTP response
    mimetype = None

    # whether to require a unicode response, please be True.
    require_unicode = True

    def __call__(self, context):
        written = self.write(context)
        if self.require_unicode:
            assert type(written) == types.UnicodeType, \
                "Writer does not write unicode. It's the 21st century. Fix it."
        return written

    def write(self, context):
        raise NotImplementedError("Where is this writer's write method?")


class TextWriter(BaseWriter):
    """Write a template context as a simple string representation.

    Test:
    >>> text = TextWriter()
    >>> response = text(test_context)
    >>> type(response)
    <type 'unicode'>
    >>> print response # doctest:+ELLIPSIS,+NORMALIZE_WHITESPACE
    {'answer': 42, 'count': ['one', 'two'],
     'lambda': <function <lambda> at 0x...>,
     'adict': {'second': 2, 'first': 1}, 'title': 'Test Title'}
    >>>
    """

    mimetype = 'text/plain'

    def write(self, context):
        return unicode(context)


class JsonWriter(BaseWriter):
    """Write a template context in JSON format.

    Note that this writer skips context keys not of a basic type and context
    values which cannot be serialized.

    See Python's json module documentation for more information.

    Test:
    >>> json = JsonWriter()
    >>> response = json(test_context)
    >>> type(response)
    <type 'unicode'>
    >>> response # doctest:+NORMALIZE_WHITESPACE
    u'{"answer": 42, "count": ["one", "two"],
       "adict": {"second": 2, "first": 1}, "title": "Test Title"}'
    >>>
    """

    mimetype = 'application/json'

    def write(self, context):
        trimmed_context = {}
        for key, value in context.items():
            try:
                json.dumps({key: value})
                trimmed_context[key] = value
            except TypeError:
                # value is not json serializable
                pass
        return unicode(json.dumps(trimmed_context))


class TemplateWriter(BaseWriter):
    """Write a template context to named template. Requires an app in context.

    The intent is to instantiate a TemplateWriter per template name, ready to
    register as a writer under the name of the template.

    Test:
    >>> from tango.factory.app import build_app
    >>> app = build_app('simplesite')
    >>> ctx = app.test_request_context()
    >>> ctx.push()
    >>> template_writer = TemplateWriter('index.html')
    >>> response = template_writer(test_context)
    >>> '<title>Test Title</title>' in response
    True
    >>> template_writer.mimetype
    'text/html'
    >>>

    The template's mimetype is guessed based on the file extension.
    >>> text_template_writer = TemplateWriter('index.txt')
    >>> print text_template_writer(test_context)
    Test Title
    >>> text_template_writer.mimetype
    'text/plain'
    >>> xml_template_writer = TemplateWriter('index.xml')
    >>> response = xml_template_writer(test_context)
    >>> '<title>Test Title</title>' in response
    True
    >>> xml_template_writer.mimetype
    'application/xml'
    >>> ctx.pop()
    >>>
    """

    mimetype = 'text/html'

    def __init__(self, template_name):
        self.template_name = template_name
        basename = self.template_name.rsplit('/', 1)[-1]
        guessed_type, guessed_encoding = mimetypes.guess_type(basename)
        if guessed_type:
            self.mimetype = guessed_type

    def write(self, context):
        return render_template(self.template_name, **context)


test_context = {'answer': 42, 'count': ['one', 'two'], 'title': 'Test Title',
                'lambda': lambda x: None, 'adict': {'first': 1, 'second': 2}}
