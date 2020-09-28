from email.message import Message
from typing import (
    TYPE_CHECKING,
    Text,
    List,
    Optional,
    Union,
    SupportsInt
)

from sifter.grammar.command import Command
from sifter.grammar.command_list import CommandList
import sifter.grammar
import sifter.handler
from sifter.validators.stringlist import StringList
from sifter.grammar.state import EvaluationState
from sifter.grammar.actions import Actions

if TYPE_CHECKING:
    from sifter.grammar.tag import Tag as TagGrammar
    from sifter.grammar.string import String
    from sifter.grammar.test import Test

__all__ = ('CommandRequire',)


# section 3.2
class CommandRequire(Command):

    RULE_IDENTIFIER: Text = 'REQUIRE'

    def __init__(
        self,
        arguments: Optional[List[Union['TagGrammar', SupportsInt, List[Union[Text, 'String']]]]] = None,
        tests: Optional[List['Test']] = None,
        block: Optional[CommandList] = None
    ) -> None:
        super(CommandRequire, self).__init__(arguments, tests, block)
        _, positional_args = self.validate_arguments(
            {},
            [StringList(), ],
        )
        self.validate_tests_size(0)
        self.validate_block_size(0)
        self.ext_names = positional_args[0]

    def evaluate(self, message: Message, state: EvaluationState) -> Optional[Actions]:
        if not isinstance(self.ext_names, list):
            raise ValueError("CommandRequire.ext_names must be a list!")
        for ext_name in self.ext_names:
            if not sifter.handler.get('extension', ext_name):
                raise RuntimeError(
                    "Required extension '%s' not supported"
                    % ext_name
                )
            state.require_extension(ext_name)
        return None


CommandRequire.register()
