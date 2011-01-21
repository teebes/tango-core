"Snapshot images of Tango content packages to speed up development cycles."

import os.path
import pickle


def build_snapshot(package_context, import_name, directory='.'):
    "Serialize a snapshot image of a Tango context package."
    # TODO: Support serializing generator / iterable objects.
    filename = get_snapshot_filename(import_name, directory)
    pickle.dump(package_context, open(filename, 'w'))
    return filename


def get_snapshot(import_name, directory='.'):
    "Deserialize a snapshot image of a Tango context package."
    filename = get_snapshot_filename(import_name, directory)
    try:
        return pickle.load(open(filename))
    except:
        return None


def get_snapshot_filename(import_name, directory):
    if directory == '.':
        return import_name + '.dat'
    return os.path.join(directory, import_name) + '.dat'
