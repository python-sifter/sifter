# type: ignore

import pytest

import sifter.comparator
from sifter.grammar.comparator import Comparator


def test_mock_comparator() -> None:
    class MockComparator(Comparator):
        COMPARATOR_ID = 'i;vnd-mock'

    MockComparator.register()
    with pytest.raises(RuntimeError):
        sifter.comparator.get_match_fn('i;vnd-mock', 'IS')
