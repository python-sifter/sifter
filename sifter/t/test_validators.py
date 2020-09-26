# type: ignore

import unittest

from sifter.grammar.tag import Tag as GrammarTag
from sifter.grammar.rule import Rule, RuleSyntaxError
from sifter.validators.number import Number
from sifter.validators.stringlist import StringList
from sifter.validators.tag import Tag as TagValidator


class MockRule(Rule):

    RULE_TYPE = 'mock'
    RULE_IDENTIFIER = 'MOCKRULE'

    def __init__(self, arguments=None, tests=None):
        super(MockRule, self).__init__(arguments, tests)


class TestValidationFn(unittest.TestCase):

    def test_too_many_args(self) -> None:
        mock_rule = MockRule([GrammarTag('IS'), 13, ])
        self.assertRaises(
            RuleSyntaxError,
            mock_rule.validate_arguments,
        )

    def test_not_enough_args(self) -> None:
        mock_rule = MockRule([13, ])
        self.assertRaises(
            RuleSyntaxError,
            mock_rule.validate_arguments,
            [
                Number(),
                StringList(),
            ],
        )


class TestTagValidator(unittest.TestCase):

    def test_allowed_tag(self) -> None:
        mock_validator = TagValidator(['MOCK', 'IS', ])
        self.assertEqual(
            mock_validator.validate([GrammarTag('IS')], 0),
            1
        )

    def test_allowed_single_tag(self) -> None:
        # test the case for a non-list single tag name
        mock_validator = TagValidator('IS')
        self.assertEqual(
            mock_validator.validate([GrammarTag('IS')], 0),
            1
        )

    def test_not_allowed_tag(self) -> None:
        mock_validator = TagValidator(['MOCK', 'FOO', ])
        self.assertEqual(
            mock_validator.validate([GrammarTag('IS')], 0),
            0
        )

    def test_not_allowed_single_tag(self) -> None:
        # test the case for a non-list single tag name. test when the tag is a
        # substring of the allowed tag.
        mock_validator = TagValidator('ISFOO')
        self.assertEqual(
            mock_validator.validate([GrammarTag('IS')], 0),
            0
        )


if __name__ == '__main__':
    unittest.main()
