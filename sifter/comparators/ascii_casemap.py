import string
try:
    # Python 3
    maketrans = str.maketrans
except AttributeError:
    # Python 2
    maketrans = string.maketrans

from sifter.comparators.octet import ComparatorOctet

__all__ = ('ComparatorASCIICasemap',)

class ComparatorASCIICasemap(ComparatorOctet):

    COMPARATOR_ID = 'i;ascii-casemap'

    @classmethod
    def sort_key(cls, s):
        return s.upper()

ComparatorASCIICasemap.register()
