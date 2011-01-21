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


class TemplateLoader(PackageLoader):
    """Template loader which looks for defaults.

    As Tango handles device detection, it will find templates implicitly here.

    Example:
    >>> environment = Environment(loader=TemplateLoader('tango.site.default'))
    >>> base = environment.get_template('base.html')
    >>> base
    <Template 'base.html'>
    >>> base.filename # doctest:+ELLIPSIS
    '.../tango/site/default/templates/base.html'
    >>> index = environment.get_template('index.html')
    >>> index
    <Template 'index.html'>
    >>> index.filename # doctest:+ELLIPSIS
    '.../tango/site/default/templates/default/index.html'
    >>>
    """

    def get_source(self, environment, template):
        try:
            return PackageLoader.get_source(self, environment, template)
        except TemplateNotFound:
            template = 'default/' + template
            return PackageLoader.get_source(self, environment, template)
