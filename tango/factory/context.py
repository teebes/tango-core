"Marshal template contexts exported declaratively by Tango content packages."

import yaml


def build_site_context(package):
    "Pull contexts from site package, discovering modules & parsing headers."


def discover_modules(package):
    "Discover content package modules, returning iterable of module objects."


def pull_context(module):
    "Pull dict template context from module, parsing it's header."


def parse_header(module):
    "Parse module header for template context metadata."
