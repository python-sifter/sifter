from email.message import Message
from typing import (
    TYPE_CHECKING,
    List,
    Optional,
    SupportsInt,
    Text,
    Union
)


from sifter.grammar.test import Test
import sifter.grammar.string
from sifter.grammar.state import EvaluationState
from sifter.validators.stringlist import StringList
from sifter.validators.tag import Comparator, MatchType

if TYPE_CHECKING:
    from sifter.grammar.tag import Tag as TagGrammar
    from sifter.grammar.string import String

__all__ = ('TestHeader',)


# section 5.7
class TestHeader(Test):

    RULE_IDENTIFIER = 'HEADER'

    def __init__(self, arguments: Optional[List[Union['TagGrammar', SupportsInt, List[Union[Text, 'String']]]]] = None, tests: Optional[List['Test']] = None) -> None:
        super(TestHeader, self).__init__(arguments, tests)
        tagged_args, positional_args = self.validate_arguments(
            {
                'comparator': Comparator(),
                'match_type': MatchType(),
            },
            [
                StringList(),
                StringList(),
            ]
        )
        self.validate_tests_size(0)

        self.headers = positional_args[0]
        self.keylist = positional_args[1]
        self.match_type: Optional['TagGrammar'] = None
        self.comparator: Optional[Union[Text, 'TagGrammar']] = None
        if 'comparator' in tagged_args:
            self.comparator = tagged_args['comparator'][1][0]  # type: ignore
        if 'match_type' in tagged_args:
            self.match_type = tagged_args['match_type'][0]  # type: ignore

    def evaluate(self, message: Message, state: EvaluationState) -> Optional[bool]:
        if not isinstance(self.headers, list):
            raise ValueError("TestHeader.headers is not a list")
        if not isinstance(self.keylist, list):
            raise ValueError("TestHeader.keylist is not a list")
        for header in self.headers:
            for value in message.get_all(header, []):
                for key in self.keylist:
                    if sifter.grammar.string.compare(
                        value,
                        key,
                        state,
                        self.comparator,
                        self.match_type
                    ):
                        return True
        return False


TestHeader.register()
