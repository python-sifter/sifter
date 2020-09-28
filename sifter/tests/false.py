from email.message import Message
from typing import (
    TYPE_CHECKING,
    List,
    Optional,
    Union,
    SupportsInt,
    Text
)

from sifter.grammar.state import EvaluationState
from sifter.grammar.test import Test

if TYPE_CHECKING:
    from sifter.grammar.tag import Tag as TagGrammar
    from sifter.grammar.string import String

__all__ = ('TestFalse',)


# section 5.6
class TestFalse(Test):

    RULE_IDENTIFIER = 'FALSE'

    def __init__(
        self,
        arguments: Optional[List[Union['TagGrammar', SupportsInt, List[Union[Text, 'String']]]]] = None,
        tests: Optional[List['Test']] = None
    ) -> None:
        super(TestFalse, self).__init__(arguments, tests)
        self.validate_arguments()
        self.validate_tests_size(0)

    def evaluate(self, message: Message, state: EvaluationState) -> Optional[bool]:
        return False


TestFalse.register()
