class SieveTag(str):

    def __str__(self):
        return ":%s" % super(SieveTag, self).__str__()

    def __repr__(self):
        return "%s('%s')" % ('SieveTag', super(SieveTag, self).__repr__())

