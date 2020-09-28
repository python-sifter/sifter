from typing import Text
from sifter.comparators.octet import ComparatorOctet

maketrans = str.maketrans

__all__ = ('ComparatorASCIICasemap',)


class ComparatorASCIICasemap(ComparatorOctet):

    COMPARATOR_ID = 'i;ascii-casemap'

    @classmethod
    def sort_key(cls, s: Text) -> Text:
        return s.upper()


ComparatorASCIICasemap.register()
