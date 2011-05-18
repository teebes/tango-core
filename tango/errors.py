"Errors and warnings reported by the Tango framework."


class HeaderException(Exception):
    "Error in parsing a module's metadata docstring."


class ConfigurationError(Exception):
    "Error in app.config, either a missing or wrongly set value."
