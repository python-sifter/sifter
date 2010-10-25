
class SieveActions(object):

    def __init__(self, implicit_keep=False):
        self.actions = []
        self.implicit_keep = implicit_keep

    def __str__(self):
        return self.actions.__str__

    def __len__(self):
        return self.actions.__len__()

    def __getitem__(self, key):
        return self.actions.__getitem__(key)

    def __iter__(self):
        return self.actions.__iter__()

    def append(self, action, action_args=None):
        self.actions.append((action, action_args))
        return self

    def cancel_implicit_keep(self):
        self.implicit_keep = False
        return self
