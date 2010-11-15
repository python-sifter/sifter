import string

import sieve.comparators.octet

class SieveComparatorASCIICasemap(sieve.comparators.octet.SieveComparatorOctet):

    COMPARATOR_ID = 'i;ascii-casemap'

    @classmethod
    def sort_key(cls, s):
        return s.translate(string.maketrans(string.ascii_lowercase,
            string.ascii_uppercase))

SieveComparatorASCIICasemap.register()
