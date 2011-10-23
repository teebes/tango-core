"Core configuration directives for Tango framework and new Tango objects."

from tango.shelf import SqliteConnector
from tango.writers import TextWriter


# Default stash shelf configuration.
SHELF_CONNECTOR_CLASS = SqliteConnector
SQLITE_FILEPATH = '/tmp/tango.db'

# Response defaults.
# It might be tempting to use a default writer class and not instance.
# But the writer is a callable not a data structure.
DEFAULT_WRITER = TextWriter()

# Date formats.
# Default date/datetime formats. If None, uses ISO 8601 format.
# See strftime table here:
# http://docs.python.org/library/datetime.html#strftime-and-strptime-behavior
DEFAULT_DATETIME_FORMAT = None
DEFAULT_DATE_FORMAT = None
