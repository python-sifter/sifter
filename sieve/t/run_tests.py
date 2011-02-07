import unittest

if __name__ == '__main__':

    suite = unittest.defaultTestLoader.loadTestsFromNames(
            (
                'sieve.t.test_comparators',
                'sieve.t.test_evaluation',
                'sieve.t.test_grammar',
                'sieve.t.test_parser',
                'sieve.t.test_validators',
            ),
        )
    unittest.TextTestRunner(verbosity=2).run(suite)

