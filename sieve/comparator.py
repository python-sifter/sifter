class SieveComparator(object):

    @classmethod
    def sort_key(cls, s):
        return s

    @classmethod
    def is(cls, str1, str2):
        raise NotImplementedError

    @classmethod
    def contains(cls, s, substring):
        raise NotImplementedError

    @classmethod
    def matches(cls, s, pattern):
        raise NotImplementedError
