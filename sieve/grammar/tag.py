class SieveTag(object):

    TAG_CACHE = {}

    def __new__(cls, tag):
        instance = SieveTag.TAG_CACHE.get(tag)
        if instance is None:
            instance = object.__new__(cls)
            instance.tag = tag
            SieveTag.TAG_CACHE[tag] = instance
        return instance

    def __str__(self):
        return ":%s" % self.tag

    def __repr__(self):
        return "%s('%s')" % (self.__class__.__name__, self.tag)

