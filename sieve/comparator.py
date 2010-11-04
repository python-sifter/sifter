class SieveComparator(object):

    @classmethod
    def sort_key(cls, s):
        return s

    @classmethod
    def cmp_is(cls, str1, str2):
        raise NotImplementedError

    @classmethod
    def cmp_contains(cls, s, substring):
        raise NotImplementedError

    @classmethod
    def cmp_matches(cls, s, pattern):
        raise NotImplementedError
