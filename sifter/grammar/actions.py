__all__ = ('Actions',)


class Actions(list):

    def __init__(self, implicit_keep: bool = False) -> None:
        super(Actions, self).__init__()
        self.implicit_keep = implicit_keep

    def append(self, action, action_args=None) -> None:
        super(Actions, self).append((action, action_args))

    def cancel_implicit_keep(self) -> 'Actions':
        self.implicit_keep = False
        return self
