import string

import sieve.comparators.octet
import sieve.handler

class SieveComparatorASCIICasemap(sieve.comparators.SieveComparatorOctet):

    @classmethod
    def sort_key(cls, s):
        return s.translate(string.maketrans(string.ascii_lowercase,
            string.ascii_uppercase))

sieve.handler.register('comparator', 'i;ascii-casemap', SieveComparatorASCIICasemap)
