import re
from typing import (
    Text,
    Optional,
    Match
)

from sifter.grammar.comparator import Comparator
from sifter.grammar.state import EvaluationState

__all__ = ('ComparatorOctet',)


class ComparatorOctet(Comparator):

    COMPARATOR_ID = 'i;octet'

    @classmethod
    def cmp_is(cls, str1: Text, str2: Text, state: EvaluationState) -> bool:
        return cls.sort_key(str1) == cls.sort_key(str2)

    @classmethod
    def cmp_contains(cls, s: Text, substring: Text, state: EvaluationState) -> bool:
        return cls.sort_key(substring) in cls.sort_key(s)

    @classmethod
    def cmp_matches(cls, s: Text, pattern: Text, state: EvaluationState) -> Optional[Match[Text]]:
        pattern = cls.sort_key(pattern)
        i, n = 0, len(pattern)
        re_pattern = []
        while i < n:
            c = pattern[i]
            i += 1
            if c == "*":
                re_pattern.append(".*")
            elif c == "?":
                re_pattern.append(".")
            elif c == "\\":
                if pattern[i:i + 1] in ("\\*", "\\?"):
                    re_pattern.append(re.escape(pattern[i + 1]))
                    i += 2
                else:
                    re_pattern.append(re.escape(c))
            else:
                re_pattern.append(re.escape(c))
        re_pattern.append(r"\Z")
        # TODO: compile and cache pattern for more efficient execution across
        # multiple strings and messages
        return re.match(
            ''.join(re_pattern),
            cls.sort_key(s),
            re.MULTILINE | re.DOTALL
        )


ComparatorOctet.register()
