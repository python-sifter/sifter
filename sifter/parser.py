from typing import (
    cast,
    Text,
    TextIO
)

import sifter.extensions.builtin  # needed by the lexer
import sifter.extensions.regex  # needed by the lexer
from sifter.grammar import grammar
from sifter.grammar import lexer
from sifter.grammar.command_list import CommandList

__all__ = ('parse_file',)


def parse_file(filehandle: TextIO) -> CommandList:
    return parse_string(filehandle.read())


def parse_string(rules: Text) -> CommandList:
    r_value = grammar.parser().parse(rules, lexer=lexer.lexer())
    return cast(CommandList, r_value)
