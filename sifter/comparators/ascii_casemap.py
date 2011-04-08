import string

from sifter.comparators.octet import ComparatorOctet

__all__ = ('ComparatorASCIICasemap',)

class ComparatorASCIICasemap(ComparatorOctet):

    COMPARATOR_ID = 'i;ascii-casemap'

    @classmethod
    def sort_key(cls, s):
        return s.translate(string.maketrans(string.ascii_lowercase,
            string.ascii_uppercase))

ComparatorASCIICasemap.register()
