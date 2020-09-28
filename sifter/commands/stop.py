from email.message import Message
from typing import (
    TYPE_CHECKING,
    Optional,
    List,
    Union,
    SupportsInt,
    Text
)

from sifter.grammar.command import Command
from sifter.grammar.command_list import CommandList
from sifter.grammar.state import EvaluationState
from sifter.grammar.actions import Actions

if TYPE_CHECKING:
    from sifter.grammar.tag import Tag as TagGrammar
    from sifter.grammar.string import String
    from sifter.grammar.test import Test

__all__ = ('CommandStop',)


# section 3.3
class CommandStop(Command):

    RULE_IDENTIFIER = 'STOP'

    def __init__(self, arguments: Optional[List[Union['TagGrammar', SupportsInt, List[Union[Text, 'String']]]]] = None, tests: Optional[List['Test']] = None, block: Optional[CommandList] = None) -> None:
        super(CommandStop, self).__init__(arguments, tests, block)
        self.validate_arguments()
        self.validate_tests_size(0)
        self.validate_block_size(0)

    def evaluate(self, message: Message, state: EvaluationState) -> Optional[Actions]:
        state.actions.append('stop')
        return None


CommandStop.register()
