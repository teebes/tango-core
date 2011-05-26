"Core Tango classes for creating applications from Tango sites."

from flask import Flask, current_app, request
from jinja2 import Environment, PackageLoader, TemplateNotFound
from werkzeug import LocalProxy as Proxy


__all__ = ['Tango', 'config', 'request', 'Proxy']


config = Proxy(lambda: current_app.config)


class Tango(Flask):
    "Application class for a Tango site."

    def __init__(self, import_name, *args, **kwargs):
        # Flask.__init__ sets static path based on sys.modules.
        # As such, import the package here to ensure it's in sys.modules.
        __import__(import_name)
        Flask.__init__(self, import_name, *args, **kwargs)

    def create_jinja_environment(self):
        options = dict(self.jinja_options)
        if 'autoescape' not in options:
            options['autoescape'] = self.select_jinja_autoescape
        return Environment(loader=TemplateLoader(self.import_name), **options)


class Route(object):
    "Route metadata for a Tango stashable context module."

    # required site field in the header
    site = None

    # required url rule/path of this route
    rule = None

    # required dict of variable names & hints to import into route's context
    exports = None

    # list of exports which are statically set in header
    static = None

    # name of writer to use in rendering route, may be template name
    writer_name = None

    # dict mapping url parameters to iterable exports providing values
    routing = None

    # dict of url parameter names & export variables to import for routing
    routing_exports = None

    # context as exported by stashable module, for template or serialization
    context = None

    # modules from which this stash module was constructed
    modules = None

    def __init__(self, site, rule, exports, static=None, writer_name=None,
                 routing=None, routing_exports=None, context=None,
                 modules=None):
        self.site = site
        self.rule = rule
        self.exports = exports
        self.static = static
        self.writer_name = writer_name

        self.routing = routing
        self.routing_exports = routing_exports

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
