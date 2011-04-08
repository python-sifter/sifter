__all__ = ('Tag',)

class Tag(str):

    def __str__(self):
        return ":%s" % super(Tag, self).__str__()

    def __repr__(self):
        return "%s('%s')" % ('Tag', super(Tag, self).__repr__())

