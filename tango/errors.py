"Errors and warnings reported by the Tango framework."


class TangoException(Exception):
    "Base exception for Tango-specific errors."


class ParseError(TangoException):
    "Error when parsing markup or scraping screens."


class NoSuchWriterException(TangoException):
    "Error when getting a response writer by a name that is not registered."


class HeaderException(TangoException):
    "Error in parsing a module's metadata docstring."


class ConfigurationError(TangoException):
    "Error in app.config, either a missing or wrongly set value."


class ModuleNotFound(TangoException):
    "Error when requiring a Python module, but it's filepath cannot be found."


class TangoWarning(Warning):
    "Base warning for Tango-specific warnings."


class DuplicateWarning(TangoWarning):
    "Base warning for reporting duplicates."


class DuplicateRouteWarning(DuplicateWarning):
    "Route is declared multiple times in a module header."


class DuplicateExportWarning(DuplicateWarning):
    "Export is declared multiple times in a module header."


class DuplicateContextWarning(DuplicateWarning):
    "Route context item is replaced by a new route context in same project."
