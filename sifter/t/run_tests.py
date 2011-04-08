import unittest

if __name__ == '__main__':

    suite = unittest.defaultTestLoader.loadTestsFromNames(
            (
                'sifter.t.test_comparators',
                'sifter.t.test_evaluation',
                'sifter.t.test_grammar',
                'sifter.t.test_parser',
                'sifter.t.test_validators',
            ),
        )
    unittest.TextTestRunner(verbosity=2).run(suite)

