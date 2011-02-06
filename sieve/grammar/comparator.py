import sieve.comparator

__all__ = ('Comparator',)

# The official definition of comparators is in RFC 4790
class Comparator(object):

    @classmethod
    def register(cls):
        try:
            sieve.comparator.register(cls.COMPARATOR_ID, cls)
        except AttributeError:
            # this method should only be called on sub-classes that define an
            # identifier
            raise NotImplementedError

    @classmethod
    def sort_key(cls, s):
        return s

