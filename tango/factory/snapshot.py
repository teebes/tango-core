"Snapshot images of Tango stash packages to speed up development cycles."

import os.path
import cPickle as pickle


def build_snapshot(app, directory='.'):
    "Serialize a snapshot image of a Tango application context."
    filename = get_snapshot_filename(app.import_name, directory)
    pickle.dump(app.routes, open(filename, 'wb'))
    return filename


def get_snapshot(import_name, directory='.'):
    "Deserialize a snapshot image of a Tango stash."
    filename = get_snapshot_filename(import_name, directory)
    try:
        return pickle.load(open(filename, 'rb'))
    except:
        return None


def get_snapshot_filename(import_name, directory):
    """Create a snapshot filename based on import name & directory.

    >>> get_snapshot_filename('sitename', '.')
    'sitename.dat'
    >>> get_snapshot_filename('sitename', '/tmp/')
    '/tmp/sitename.dat'
    >>>
    """
    if directory == '.':
        return import_name + '.dat'
    return os.path.join(directory, import_name) + '.dat'
