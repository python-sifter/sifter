
class SieveActions(object):

    def __init__(self, implicit_keep=False):
        self.actions = []
        self.implicit_keep = implicit_keep

    def append(self, action, action_args=None):
        self.actions.append((action, action_args))
        return self

    def cancel_implicit_keep(self):
        self.implicit_keep = False
        return self

    def __getattr__(self, name):
        return getattr(self.actions, name)
