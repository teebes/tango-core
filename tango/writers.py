"""Response writers, which take a template context and return a string.

A response writer is a callable with a signature:

    writer(template_context, <required_positional_arguments>, **options)

All response writers require a template context dictionary as the first
argument.  Should you want a blank response, provide an empty dictionary.  Some
writers require additional arguments, and these are taken as positional
arguments after the template context.

All response writers accept keyword arguments of arbitrary length, even if no
keyword arguments are used.
"""

def json(context, **options):
    pass


def text(context, **options):
    pass


def template(context, template_name, **options):
    pass
