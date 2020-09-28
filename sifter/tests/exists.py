from email.message import Message
from typing import (
    TYPE_CHECKING,
    List,
    Optional,
    SupportsInt,
    Text,
    Union
)


from sifter.grammar.state import EvaluationState
from sifter.grammar.test import Test
from sifter.validators.stringlist import StringList

if TYPE_CHECKING:
    from sifter.grammar.tag import Tag as TagGrammar
    from sifter.grammar.string import String

__all__ = ('TestExists',)


# section 5.9
class TestExists(Test):

    RULE_IDENTIFIER = 'EXISTS'

    def __init__(self, arguments: Optional[List[Union['TagGrammar', SupportsInt, List[Union[Text, 'String']]]]] = None, tests: Optional[List['Test']] = None) -> None:
        super(TestExists, self).__init__(arguments, tests)
        tagged_args, positional_args = self.validate_arguments(
            {},
            [StringList(), ]
        )
        self.validate_tests_size(0)
        self.headers = positional_args[0]

    def evaluate(self, message: Message, state: EvaluationState) -> Optional[bool]:
        if not isinstance(self.headers, list):
            raise ValueError("TestExists.headers must be a list")
        for header in self.headers:
            if header not in message:
                return False
        return True


TestExists.register()
