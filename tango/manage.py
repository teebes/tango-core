"Console entry point and management & development tasks for Tango framework."

import os
import sys

from flaskext.script import Command, Option
from flaskext.script import Manager as BaseManager
from flaskext.script import Server as BaseServer
from flaskext.script import Shell as BaseShell

from tango.app import Tango
from tango.factory.app import get_app
from tango.factory.snapshot import build_snapshot
from tango.imports import module_exists
import tango
import tango.factory.stash

commands = []


def validate_site(site):
    "Verify site exists, and abort if it does not."
    if not module_exists(site):
        print "Cannot find site '%s'." % site
        # /usr/include/sysexits.h defines EX_NOINPUT 66 as: cannot open input
        sys.exit(66)


def command(function):
    """Decorator to mark a function as a Tango subcommand.

    The function's docstring is its usage string;
    its function signature, its command-line arguments.
    """
    commands.append(function)
    return function


@command
def version():
    'Display this version of Tango.'
    print tango.__label__


@command
def snapshot(site):
    "Pull context from a stashable Tango site and store it into an image file."
    validate_site(site)
    app = get_app(site, import_stash=True, use_snapshot=False)
    filename = build_snapshot(app)
    print 'Snapshot of full stashable template context:', filename


@command
def shelve(site):
    "Shelve an application's stash, as a worker process."
    validate_site(site)
    tango.factory.stash.shelve(site, report_file=sys.stdout)


class Manager(BaseManager):
    def handle(self, prog, *args, **kwargs):
        # Chop off full path to program name in argument parsing.
        prog = os.path.basename(prog)
        return BaseManager.handle(self, prog, *args, **kwargs)


class Server(BaseServer):
    description = "Run a Tango site on the local machine, for development."

    def get_options(self):
        return (Option('site'),) + BaseServer.get_options(self)

    def handle(self, _, site, host, port, use_debugger, use_reloader):
        validate_site(site)
        app = get_app(site)
        app.run(host=host, port=port, debug=use_debugger,
                use_debugger=use_debugger, use_reloader=use_reloader,
                **self.server_options)


class Shell(BaseShell):
    description = 'Runs a Python shell inside Tango application context.'

    def get_options(self):
        return (Option('site'),) + BaseShell.get_options(self)

    def handle(self, _, site, *args, **kwargs):
        validate_site(site)
        app = get_app(site)
        Command.handle(self, app, *args, **kwargs)


def run():
    sys.path.append('.')
    # Create a Manager instance to parse arguments & marshal commands.
    manager = Manager(Tango(__name__), with_default_commands=False)

    manager.add_command('serve', Server())
    manager.add_command('shell', Shell())
    for cmd in commands:
        manager.command(cmd)
    manager.run()
