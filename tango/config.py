"Core configuration directives for Tango framework and new Tango objects."

import os

# Build defaults.

TANGO_BUILD_BASE = os.getcwd()
TANGO_BUILD_DIR = 'public'

# Date formats.
# Default date/datetime formats. If None, uses ISO 8601 format.
# See strftime table here:
# http://docs.python.org/library/datetime.html#strftime-and-strptime-behavior
DEFAULT_DATETIME_FORMAT = None
DEFAULT_DATE_FORMAT = None
