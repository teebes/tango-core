"Shelf connectors for persisting stashed template context variables."

class BaseConnector(object):
    def __init__(self, app):
        self.app = app

    def get(self, site, rule):
        raise NotImplementedError('A shelf connector must implement get.')

    def put(self, site, rule, context):
        raise NotImplementedError('A shelf connector must implement put.')
