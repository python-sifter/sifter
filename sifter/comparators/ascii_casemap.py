from sifter.comparators.octet import ComparatorOctet

maketrans = str.maketrans

__all__ = ('ComparatorASCIICasemap',)


class ComparatorASCIICasemap(ComparatorOctet):

    COMPARATOR_ID = 'i;ascii-casemap'

    @classmethod
    def sort_key(cls, s):
        return s.upper()


ComparatorASCIICasemap.register()
