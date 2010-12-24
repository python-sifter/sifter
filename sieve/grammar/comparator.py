import sieve.handler

__all__ = ('Comparator',)

class Comparator(object):

    @classmethod
    def register(cls):
        try:
            sieve.handler.register('comparator', cls.COMPARATOR_ID, cls)
        except AttributeError:
            # this method should only be called on sub-classes that define an
            # identifier
            raise NotImplementedError

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
