import unittest

import sifter.comparator
import sifter.grammar


class MockComparator(sifter.grammar.Comparator):

    COMPARATOR_ID = 'i;vnd-mock'


class TestMatchTypes(unittest.TestCase):

    def setUp(self):
        MockComparator.register()

    def test_unimplemented_match_type(self):
        self.assertRaises(
                RuntimeError,
                sifter.comparator.get_match_fn,
                'i;vnd-mock', 'IS',
            )


if __name__ == '__main__':
    unittest.main()
