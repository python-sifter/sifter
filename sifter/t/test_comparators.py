# type: ignore

import unittest

import sifter.comparator
from sifter.grammar.comparator import Comparator


class MockComparator(Comparator):

    COMPARATOR_ID = 'i;vnd-mock'


class TestMatchTypes(unittest.TestCase):

    def setUp(self) -> None:
        MockComparator.register()

    def test_unimplemented_match_type(self) -> None:
        self.assertRaises(
            RuntimeError,
            sifter.comparator.get_match_fn,
            'i;vnd-mock', 'IS',
        )


if __name__ == '__main__':
    unittest.main()
