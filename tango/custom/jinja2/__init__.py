from jinja2 import Environment as BaseEnvironment

class Environment(BaseEnvironment):
    def has_template(self, template):
        try:
            self.get_template(template)
        except:
            return False
        return True
