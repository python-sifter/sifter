from typing import (
    TYPE_CHECKING,
    Text,
    Optional,
    List
)

import sifter.grammar
from sifter.grammar.command_list import CommandList
from sifter.grammar.rule import Rule, RuleSyntaxError
import sifter.utils

if TYPE_CHECKING:
    from sifter.grammar.tag import Tag

__all__ = ('Command',)


class Command(Rule):

    RULE_TYPE: Text = 'command'

    def __init__(self, arguments: Optional[List['Tag']] = None, tests=None, block=None) -> None:
        super(Command, self).__init__(arguments, tests)
        if block is None:
            self.block = CommandList()
        else:
            self.block = block

    def __str__(self) -> Text:
        s = [super(Command, self).__str__(), ]
        if len(self.block.commands) > 0:
            s.append("{\n")
            for command in self.block.commands:
                s.append(sifter.utils.indent_string(str(command), 2))
            s.append("}\n")
        return ''.join(s)

    def validate_block_size(self, max_commands: int) -> None:
        if len(self.block.commands) > max_commands:
            raise RuleSyntaxError(
                "%s takes no more than %d commands" % (self.RULE_IDENTIFIER, max_commands)
            )
