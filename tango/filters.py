from time import mktime
from datetime import datetime as dt

from flask import current_app


UNSET = object()
filters = {}


def init_app(app):
    "Load filters registered in this module onto given app object."
    app.jinja_env.filters.update(filters)
    return app


def register(f):
    "Decorator to register given function to load onto app via init_app."
    filters[f.__name__] = f
    return f


def get_default(key):
    """Get a default value from the current app's configuration.

    Currently returns None when no app is in context:
    >>> get_default('NO_APP_IS_LOADED') is None
    True
    >>>
    """
    try:
        return current_app.config.get(key, None)
    except (AttributeError, RuntimeError):
        # AttributeError or RuntimeError depending on upstream versions.
        # No app is in context, return None as documented.
        return None


@register
def datetime(a_date_or_datetime, format=UNSET):
    "Filter which formats given datetime/date using given format option."
    if format is UNSET:
        format = get_default('DEFAULT_DATETIME_FORMAT')
    if format is None:
        return str(a_date_or_datetime)
    return a_date_or_datetime.strftime(format)


@register
def date(a_date, format=UNSET):
    "Filter which formats given datetime/date using given format option."
    if format is UNSET:
        format = get_default('DEFAULT_DATE_FORMAT')
    return datetime(a_date, format=format)


@register
def struct_time(a_struct_time, format=UNSET):
    "Filter which formats given struct_time using given format option."
    a_date = dt.fromtimestamp(mktime(a_struct_time))
    if format is UNSET:
        format = get_default('DEFAULT_DATETIME_FORMAT')
    return datetime(a_date, format=format)
