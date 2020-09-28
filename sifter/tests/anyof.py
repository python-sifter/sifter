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


__all__ = ('TestAnyOf',)


# section 5.3
class TestAnyOf(Test):

    RULE_IDENTIFIER = 'ANYOF'

    def __init__(
        self,
        arguments: Optional[List[Union['TagGrammar', SupportsInt, List[Union[Text, 'String']]]]] = None,
        tests: Optional[List['Test']] = None
    ) -> None:
        super(TestAnyOf, self).__init__(arguments, tests)
        self.validate_arguments()

    def evaluate(self, message: Message, state: EvaluationState) -> Optional[bool]:
        # short-circuit evaluation if a test is true. the base standard does
        # not specify if all tests must be evaluated or in what order, but the
        # "ihave" extension requires short-circuit left-to-right evaluation
        # (RFC 5463, section 4). so we might as well do that.
        for test in self.tests:
            if test.evaluate(message, state):
                return True
        return False


TestAnyOf.register()
