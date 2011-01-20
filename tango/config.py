"Core configuration directives for Tango framework and new Tango objects."

import tango.version


TANGO_VERSION = tango.version.info.banner
TANGO_MAINTAINER = tango.version.info.maintainer_info
TANGO_LABEL = tango.version.info.label

# Default date/datetime formats. If None, uses ISO 8601 format.
# See strftime table here:
# http://docs.python.org/library/datetime.html#strftime-and-strptime-behavior
DEFAULT_DATETIME_FORMAT = None
DEFAULT_DATE_FORMAT = None
