import operator
from email.message import Message
from typing import (
    TYPE_CHECKING,
    Any,
    List,
    Callable,
    Dict,
    Text,
    SupportsInt,
    Optional,
    Union
)

from sifter.grammar.test import Test
from sifter.validators.tag import Tag
from sifter.validators.number import Number
from sifter.grammar.state import EvaluationState

if TYPE_CHECKING:
    from sifter.grammar.tag import Tag as TagGrammar
    from sifter.grammar.string import String

__all__ = ('TestSize',)


# section 5.9
class TestSize(Test):

    RULE_IDENTIFIER = 'SIZE'

    COMPARISON_FNS: Dict[Text, Callable[[Any, Any], bool]] = {
        'OVER': operator.gt,
        'UNDER': operator.lt,
    }

    def __init__(self, arguments: Optional[List[Union['TagGrammar', SupportsInt, List[Union[Text, 'String']]]]] = None, tests: Optional[List['Test']] = None) -> None:
        super(TestSize, self).__init__(arguments, tests)
        tagged_args, positional_args = self.validate_arguments(
            {
                'size': Tag(
                    ('OVER', 'UNDER'),
                    (Number(),)
                ),
            }
        )
        self.validate_tests_size(0)
        self.comparison_fn = TestSize.COMPARISON_FNS[tagged_args['size'][0]]  # type: ignore
        self.comparison_size = tagged_args['size'][1]

    def evaluate(self, message: Message, state: EvaluationState) -> Optional[bool]:
        # FIXME: size is defined as number of octets, whereas this gives us
        # number of characters
        message_size = len(message.as_string())
        return self.comparison_fn(message_size, self.comparison_size)


TestSize.register()
