import unittest

import sifter.grammar
import sifter.validators

class MockRule(sifter.grammar.Rule):

    RULE_TYPE = 'mock'
    RULE_IDENTIFIER = 'MOCKRULE'

    def __init__(self, arguments=None, tests=None):
        super(MockRule, self).__init__(arguments, tests)

class TestValidationFn(unittest.TestCase):

    def test_too_many_args(self):
        mock_rule = MockRule([ sifter.grammar.Tag('IS'), 13, ])
        self.assertRaises(
                sifter.grammar.RuleSyntaxError,
                mock_rule.validate_arguments,
            )

    def test_not_enough_args(self):
        mock_rule = MockRule([ 13, ])
        self.assertRaises(
                sifter.grammar.RuleSyntaxError,
                mock_rule.validate_arguments,
                [
                    sifter.validators.Number(),
                    sifter.validators.StringList(),
                ],
            )

class TestTagValidator(unittest.TestCase):

    def test_allowed_tag(self):
        mock_validator = sifter.validators.Tag(['MOCK', 'IS',])
        self.assertEqual(
                mock_validator.validate([sifter.grammar.Tag('IS')], 0),
                1)

    def test_allowed_single_tag(self):
        # test the case for a non-list single tag name
        mock_validator = sifter.validators.Tag('IS')
        self.assertEqual(
                mock_validator.validate([sifter.grammar.Tag('IS')], 0),
                1)

    def test_not_allowed_tag(self):
        mock_validator = sifter.validators.Tag(['MOCK', 'FOO',])
        self.assertEqual(
                mock_validator.validate([sifter.grammar.Tag('IS')], 0),
                0)

    def test_not_allowed_single_tag(self):
        # test the case for a non-list single tag name. test when the tag is a
        # substring of the allowed tag.
        mock_validator = sifter.validators.Tag('ISFOO')
        self.assertEqual(
                mock_validator.validate([sifter.grammar.Tag('IS')], 0),
                0)


if __name__ == '__main__':
    unittest.main()
