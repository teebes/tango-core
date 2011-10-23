"Shelf connectors for persisting stashed template context variables."

import cPickle as pickle
import pickletools
from contextlib import closing
from cPickle import HIGHEST_PROTOCOL
from sqlite3 import Binary as blobify
from sqlite3 import dbapi2 as sqlite3


class BaseConnector(object):
    def __init__(self, app):
        self.app = app

    def get(self, site, rule):
        raise NotImplementedError('A shelf connector must implement get.')

    def put(self, site, rule, context):
        raise NotImplementedError('A shelf connector must implement put.')


class SqliteConnector(BaseConnector):
    def initialize(self):
        """ -- schema:
        CREATE TABLE contexts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            site TEXT NOT NULL,
            rule TEXT NOT NULL,
            context BLOB NOT NULL
        );
        """
        with self.connect(initialize=False) as db:
            cursor = db.execute("SELECT name FROM sqlite_master "
                                "WHERE type='table' AND name='contexts';")
            if cursor.fetchone() is None:
                db.cursor().executescript(self.initialize.func_doc)

    def connect(self, initialize=True):
        if initialize:
            self.initialize()
        return sqlite3.connect(self.app.config['SQLITE_FILEPATH'])

    def connection(self):
        return closing(self.connect())

    def get(self, site, rule):
        with self.connection() as db:
            cursor = db.execute('SELECT context FROM contexts '
                                'WHERE site = ? AND rule = ? '
                                'ORDER BY id DESC;', (site, rule))
            result = cursor.fetchone()
            if result is None:
                return {}
            return pickle.loads(str(result[0]))

    def put(self, site, rule, context):
        with self.connection() as db:
            # Check to see if the context is already shelved.
            cursor = db.execute('SELECT id FROM contexts '
                                'WHERE site = ? AND rule = ?;', (site, rule))
            serialized = pickle.dumps(context, HIGHEST_PROTOCOL)
            # Optimize pickle size, and conform it to sqlite's BLOB type.
            serialized = blobify(pickletools.optimize(serialized))
            if cursor.fetchone() is None:
                db.execute('INSERT INTO contexts '
                           '(site, rule, context) VALUES (?, ?, ?);',
                           (site, rule, serialized))
            else:
                db.execute('UPDATE contexts '
                           'SET context = ? '
                           'WHERE site = ? AND rule = ?;',
                           (serialized, site, rule))
            db.commit()
