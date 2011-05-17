import unittest

import sifter.grammar
import sifter.validators

class MockRule(sifter.grammar.Rule):

    RULE_TYPE = 'mock'
    RULE_IDENTIFIER = 'MOCKRULE'

    def __init__(self, arguments=None, tests=None):
        super(MockRule, self).__init__(arguments, tests)

class TestArgValidator(unittest.TestCase):

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

    def test_allowed_tag(self):
        mock_rule = MockRule([ sifter.grammar.Tag('IS'), ])
        tag_args, pos_args = mock_rule.validate_arguments(
                { 'mock_tag' : sifter.validators.Tag(['MOCK', 'IS',]), },
            )
        self.assertTrue('mock_tag' in tag_args)
        self.assertEqual(len(pos_args), 0)
        # test the case for a non-list single tag name
        tag_args, pos_args = mock_rule.validate_arguments(
                { 'mock_tag' : sifter.validators.Tag('IS'), },
            )
        self.assertTrue('mock_tag' in tag_args)
        self.assertEqual(len(pos_args), 0)

    def test_not_allowed_tag(self):
        mock_rule = MockRule([ sifter.grammar.Tag('IS'), ])
        self.assertRaises(
                sifter.grammar.RuleSyntaxError,
                mock_rule.validate_arguments,
                { 'mock_tag' : sifter.validators.Tag(['MOCK', 'FOO',]), },
            )
        # test the case for a non-list single tag name. test when the tag is a
        # substring of the allowed tag.
        self.assertRaises(
                sifter.grammar.RuleSyntaxError,
                mock_rule.validate_arguments,
                { 'mock_tag' : sifter.validators.Tag('ISFOO'), },
            )


if __name__ == '__main__':
    unittest.main()
