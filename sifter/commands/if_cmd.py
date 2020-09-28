from email.message import Message
from typing import (
    TYPE_CHECKING,
    List,
    Optional,
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

__all__ = ('CommandIf', 'CommandElsIf', 'CommandElse',)


# section 3.1
class CommandIfBase(Command):

    def __init__(self, arguments: Optional[List[Union['TagGrammar', SupportsInt, List[Union[Text, 'String']]]]] = None, tests: Optional[List['Test']] = None, block: Optional[CommandList] = None) -> None:
        super(CommandIfBase, self).__init__(arguments, tests, block)
        self.validate_arguments()
        self.validate_tests_size(1)

    def evaluate(self, message: Message, state: EvaluationState) -> Optional[Actions]:
        if self.tests[0].evaluate(message, state):
            result = self.block.evaluate(message, state)
            state.last_if = True
            return result
        state.last_if = False
        return None


class CommandIf(CommandIfBase):

    RULE_IDENTIFIER = 'IF'


CommandIf.register()


class CommandElsIf(CommandIfBase):

    RULE_IDENTIFIER = 'ELSIF'

    def evaluate(self, message: Message, state: EvaluationState) -> Optional[Actions]:
        if state.last_if:
            return None
        return super(CommandElsIf, self).evaluate(message, state)


CommandElsIf.register()


class CommandElse(Command):

    RULE_IDENTIFIER = 'ELSE'

    def __init__(self, arguments: Optional[List[Union['TagGrammar', SupportsInt, List[Union[Text, 'String']]]]] = None, tests: Optional[List['Test']] = None, block: Optional[CommandList] = None) -> None:
        super(CommandElse, self).__init__(arguments, tests, block)
        self.validate_arguments()
        self.validate_tests_size(0)

    def evaluate(self, message: Message, state: EvaluationState) -> Optional[Actions]:
        if state.last_if:
            return None
        return self.block.evaluate(message, state)


CommandElse.register()
