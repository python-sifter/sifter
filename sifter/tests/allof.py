from email.message import Message
from typing import (
    TYPE_CHECKING,
    Text,
    List,
    Optional,
    Union,
    SupportsInt
)

from sifter.grammar.test import Test
from sifter.grammar.state import EvaluationState

if TYPE_CHECKING:
    from sifter.grammar.tag import Tag as TagGrammar
    from sifter.grammar.string import String

__all__ = ('TestAllOf',)


# section 5.2
class TestAllOf(Test):

    RULE_IDENTIFIER: Text = 'ALLOF'

    def __init__(
        self,
        arguments: Optional[List[Union['TagGrammar', SupportsInt, List[Union[Text, 'String']]]]] = None,
        tests: Optional[List['Test']] = None
    ) -> None:
        super(TestAllOf, self).__init__(arguments, tests)
        self.validate_arguments()

    def evaluate(self, message: Message, state: EvaluationState) -> Optional[bool]:
        # short-circuit evaluation if a test is false. the base standard does
        # not specify if all tests must be evaluated or in what order, but the
        # "ihave" extension requires short-circuit left-to-right evaluation
        # (RFC 5463, section 4). so we might as well do that.
        for test in self.tests:
            if not test.evaluate(message, state):
                return False
        return True


TestAllOf.register()
