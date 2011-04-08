import unittest

import sifter.grammar
import sifter.validators

class MockRule(sifter.grammar.Rule):

    RULE_TYPE = 'mock'
    RULE_IDENTIFIER = 'MOCKRULE'

    def __init__(self, arguments=None, tests=None):
        super(MockRule, self).__init__(arguments, tests)

class TestArgValidator(unittest.TestCase):

    def setUp(self):
        self.mock_rule = MockRule([ sifter.grammar.Tag('IS'), 13, ])

    def test_too_many_args(self):
        self.assertRaises(
                sifter.grammar.RuleSyntaxError,
                self.mock_rule.validate_arguments,
            )

    def test_not_enough_args(self):
        self.assertRaises(
                sifter.grammar.RuleSyntaxError,
                self.mock_rule.validate_arguments,
                { 'match_type' : sifter.validators.MatchType(), },
                [
                    sifter.validators.Number(),
                    sifter.validators.StringList(),
                ],
            )

if __name__ == '__main__':
    unittest.main()
