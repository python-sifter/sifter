from typing import Text

__all__ = ('Tag',)


class Tag(str):

    def __str__(self) -> Text:
        return ":%s" % super(Tag, self).__str__()

    def __repr__(self) -> Text:
        return "%s('%s')" % ('Tag', super(Tag, self).__repr__())
