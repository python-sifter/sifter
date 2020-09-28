from email.message import Message
from typing import (
    TYPE_CHECKING,
    List,
    Optional,
    Union,
    SupportsInt,
    Text
)

from sifter.grammar.test import Test
from sifter.grammar.state import EvaluationState

if TYPE_CHECKING:
    from sifter.grammar.tag import Tag as TagGrammar
    from sifter.grammar.string import String

__all__ = ('TestNot',)


# section 5.8
class TestNot(Test):

    RULE_IDENTIFIER = 'NOT'

    def __init__(self, arguments: Optional[List[Union['TagGrammar', SupportsInt, List[Union[Text, 'String']]]]] = None, tests: Optional[List['Test']] = None) -> None:
        super(TestNot, self).__init__(arguments, tests)
        self.validate_arguments()
        self.validate_tests_size(1)

    def evaluate(self, message: Message, state: EvaluationState) -> Optional[bool]:
        return not self.tests[0].evaluate(message, state)


TestNot.register()
