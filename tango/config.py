"Core configuration directives for Tango framework and new Tango objects."

import os

from tango.writers import TextWriter


# Response defaults.
DEFAULT_WRITER = TextWriter()

# Date formats.
# Default date/datetime formats. If None, uses ISO 8601 format.
# See strftime table here:
# http://docs.python.org/library/datetime.html#strftime-and-strptime-behavior
DEFAULT_DATETIME_FORMAT = None
DEFAULT_DATE_FORMAT = None
