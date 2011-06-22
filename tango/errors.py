"Errors and warnings reported by the Tango framework."


class ParseError(Exception):
    "Error when parsing markup or scraping screens."


class NoSuchWriterException(Exception):
    "Error when getting a response writer by a name that is not registered."


class HeaderException(Exception):
    "Error in parsing a module's metadata docstring."


class ConfigurationError(Exception):
    "Error in app.config, either a missing or wrongly set value."


class DuplicateWarning(Warning):
    "Base warning for reporting duplicates."


class DuplicateRouteWarning(DuplicateWarning):
    "Route is declared multiple times in a module header."


class DuplicateExportWarning(DuplicateWarning):
    "Export is declared multiple times in a module header."


class DuplicateRoutingWarning(DuplicateWarning):
    "Routing is declared multiple times in a module header."


class DuplicateContextWarning(DuplicateWarning):
    "Route context item is replaced by a new route context in same project."
