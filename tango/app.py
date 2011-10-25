"Core Tango classes for creating applications from Tango sites."

from flask import Flask, current_app, request, _request_ctx_stack
from jinja2 import Environment, PackageLoader, TemplateNotFound
from werkzeug import LocalProxy as Proxy
from werkzeug.utils import get_content_type

import tango
from tango.errors import NoSuchWriterException
from tango.imports import module_is_package
from tango.writers import TemplateWriter, TextWriter, JsonWriter


__all__ = ['Tango', 'config', 'request', 'Proxy']


config = Proxy(lambda: current_app.config)


class Tango(Flask):
    "Application class for a Tango site."

    def __init__(self, import_name, *args, **kwargs):
        if module_is_package(import_name):
            # Flask.__init__ sets static path based on sys.modules.
            # As such, import the package here to ensure it's in sys.modules.
            __import__(import_name)
        Flask.__init__(self, import_name, *args, **kwargs)
        self.set_default_config()
        self.writers = {}
        self.register_default_writers()

    def set_default_config(self):
        self.config.from_object('tango.config')
        self.config['TANGO_VERSION'] = tango.__fullversion__
        self.config['TANGO_MAINTAINER'] = tango.__contact__

    def create_jinja_environment(self):
        options = dict(self.jinja_options)
        if 'autoescape' not in options:
            options['autoescape'] = self.select_jinja_autoescape
        return Environment(loader=TemplateLoader(self.import_name), **options)

    def register_default_writers(self):
        self.register_writer('text', TextWriter())
        self.register_writer('json', JsonWriter())

    def register_writer(self, name, writer):
        self.writers[name] = writer

    def writer(self, a_callable):
        """Decorator to register a callable as a response writer.

        The writer must take one argument, a template context dictionary,
        and should return a unicode instance.

        Test:
        >>> app = Tango('simplesite')
        >>> app.writers.get('my_writer')
        >>> @app.writer
        ... def my_writer(context):
        ...     return unicode(context)
        ...
        >>> app.writers.get('my_writer') # doctest:+ELLIPSIS
        <function my_writer at 0x...>
        >>>
        """
        self.register_writer(a_callable.__name__, a_callable)
        return a_callable

    def get_writer(self, name):
        # Do not register writer for None, in case of config change.
        if name is None:
            return self.config['DEFAULT_WRITER']
        writer = self.writers.get(name)
        if writer is not None:
            return writer
        # A writer prefixed with 'template:' is for a template.
        if name.startswith('template:'):
            template_name = name.replace('template:', '', 1)
            writer = TemplateWriter(template_name)
            self.register_writer(name, writer)
            return writer
        raise NoSuchWriterException(name)

    @property
    def connector(self):
        return self.config['SHELF_CONNECTOR_CLASS'](self)

    def build_view(self, route, **options):
        site = route.site
        rule = route.rule
        writer = self.get_writer(route.writer_name)
        def view(*args, **kwargs):
            ctx = _request_ctx_stack.top
            ctx.mimetype = writer.mimetype
            return writer.write(self.connector.get(site, rule))
        view.__name__ = route.rule
        return self.route(route.rule, **options)(view)

    def process_response(self, response):
        """Inject mimetype into response before it's sent to the WSGI server.

        This is only intended for stashable view functions, created by
        :meth:`Tango.build_view`.
        """
        Flask.process_response(self, response)
        ctx = _request_ctx_stack.top
        if hasattr(ctx, 'mimetype'):
            mimetype, charset = (ctx.mimetype, response.charset)
            response.content_type = get_content_type(mimetype, charset)
            response.headers['Content-Type'] = response.content_type
        return response

    @property
    def version(self):
        """Application version information, Tango versioning by default.

        Test:
        >>> app = Tango('simplesite')
        >>> print app.version # doctest:+ELLIPSIS
        Tango ...
        Maintainer: ...
        >>>
        """
        return tango.build_label(self.config['TANGO_VERSION'],
                                 self.config['TANGO_MAINTAINER'])


class Route(object):
    "Route metadata for a Tango stashable context module."

    # required site field in the header
    site = None

    # required url rule/path of this route
    rule = None

    # required dict of variable names & values imported into route's context
    # an export's value is None when it has not yet been imported
    exports = None

    # list of exports which are statically set in header
    static = None

    # name of writer to use in rendering route, may be template name
    writer_name = None

    # context as exported by stashable module, for template or serialization
    context = None

    # modules from which this stash module was constructed
    modules = None

    def __init__(self, site, rule, exports, static=None, writer_name=None,
                 context=None, modules=None):
        self.site = site
        self.rule = rule
        self.exports = exports
        self.static = static
        self.writer_name = writer_name

        self.context = context
        self.modules = modules

    def __repr__(self):
        pattern = u'<Route: {0}{1}>'
        if self.writer_name is None:
            return pattern.format(self.rule, '')
        else:
            return pattern.format(self.rule, ', {0}'.format(self.writer_name))


class TemplateLoader(PackageLoader):
    """Template loader which looks for defaults.

    As Tango handles device detection, it will find templates implicitly here.

    Example:
    >>> environment = Environment(loader=TemplateLoader('simplesite'))
    >>> base = environment.get_template('base.html')
    >>> base
    <Template 'base.html'>
    >>> base.filename # doctest:+ELLIPSIS
    '.../simplesite/templates/base.html'
    >>> index = environment.get_template('index.html')
    >>> index
    <Template 'index.html'>
    >>> index.filename # doctest:+ELLIPSIS
    '.../simplesite/templates/default/index.html'
    >>>
    """

    def get_source(self, environment, template):
        try:
            return PackageLoader.get_source(self, environment, template)
        except TemplateNotFound:
            template = 'default/' + template
            return PackageLoader.get_source(self, environment, template)
