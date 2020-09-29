# type: ignore


import pytest

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


def test_too_many_args() -> None:
    mock_rule = MockRule([GrammarTag('IS'), 13, ])
    with pytest.raises(RuleSyntaxError):
        mock_rule.validate_arguments()


def test_not_enough_args() -> None:
    mock_rule = MockRule([13, ])
    with pytest.raises(RuleSyntaxError):
        mock_rule.validate_arguments([
            Number(),
            StringList(),
        ])


def test_allowed_tag() -> None:
    mock_validator = TagValidator(['MOCK', 'IS', ])
    assert mock_validator.validate([GrammarTag('IS')], 0) == 1


def test_allowed_single_tag() -> None:
    # test the case for a non-list single tag name
    mock_validator = TagValidator('IS')
    assert mock_validator.validate([GrammarTag('IS')], 0) == 1


def test_not_allowed_tag() -> None:
    mock_validator = TagValidator(['MOCK', 'FOO', ])
    assert mock_validator.validate([GrammarTag('IS')], 0) == 0


def test_not_allowed_single_tag() -> None:
    # test the case for a non-list single tag name. test when the tag is a
    # substring of the allowed tag.
    mock_validator = TagValidator('ISFOO')
    assert mock_validator.validate([GrammarTag('IS')], 0) == 0
