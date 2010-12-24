import string

from sieve.comparators.octet import SieveComparatorOctet

__all__ = ('SieveComparatorASCIICasemap',)

class SieveComparatorASCIICasemap(SieveComparatorOctet):

    COMPARATOR_ID = 'i;ascii-casemap'

    @classmethod
    def sort_key(cls, s):
        return s.translate(string.maketrans(string.ascii_lowercase,
            string.ascii_uppercase))

SieveComparatorASCIICasemap.register()
