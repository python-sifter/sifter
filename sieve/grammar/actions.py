__all__ = ('Actions',)

class Actions(list):

    def __init__(self, implicit_keep=False):
        super(Actions, self).__init__()
        self.implicit_keep = implicit_keep

    def append(self, action, action_args=None):
        super(Actions, self).append((action, action_args))
        return self

    def cancel_implicit_keep(self):
        self.implicit_keep = False
        return self
