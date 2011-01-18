"Console entry point and management & development tasks for Tango framework."

from functools import update_wrapper

from flaskext.script import Manager

from tango.app import Tango
import tango.factory


class Version(object):
    "Version management class for flexibility in project versioning metadata."
    number = '0.1'
    name = 'Basico'
    notice = 'dev' # Set to '' on release.
    maintainer = 'Ron DuPlain'
    maintainer_email = 'ron.duplain@willowtreeapps.com'

    @property
    def label(self):
        return ('Tango %(number)s (%(name)s) %(notice)s\n'
                'Maintainer: %(maintainer)s <%(maintainer_email)s>'
                % type(self).__dict__)


version = Version()
commands = []


def create_app(site):
    try:
        return tango.factory.create_app('tango.site.' + site)
    except ImportError:
        return tango.factory.create_app(site)


def command(function):
    """Decorator to mark a function as a Tango subcommand.

    The function's docstring is its usage string;
    its function signature, its command-line arguments.
    """
    commands.append(function)
    return function


def register_command(name):
    "Like @command, but allows for renaming functions."
    def decorator(function):
        function.__name__ = name
        return command(function)
    return decorator


def require_site(function):
    """Decorator to mark a function as requiring a Tango site package.

    The first argument of the decorated function is translated from a Tango
    package name into a Tango app instance, i.e.

    tango.site.default -> Tango('tango.site.default')
    """
    def wrapper(site, *args, **kwargs):
        app = create_app(site)
        return function(app, *args, **kwargs)
    update_wrapper(wrapper, function)
    return wrapper


@register_command('version')
def print_version():
    'Display this version of Tango.'
    print version.label


@command
@require_site
def snapshot(app):
    "Build context from a Tango site package and store it into an image file."


@command
@require_site
def build(app):
    "Build a Tango site into a collection of static files."


@command
@require_site
def serve(app):
    "Run a Tango site on the local machine, for development."


@command
@require_site
def shell(app):
    "Open an interactive interpreter within a Tango site request context."


def run():
    manager = Manager(Tango(__name__), with_default_commands=False)

    for registered_command in commands:
        manager.command(registered_command)
    manager.run()
