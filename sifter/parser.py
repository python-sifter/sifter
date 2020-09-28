from typing import (
    cast,
    TextIO
)

import sifter.extensions.builtin  # needed by the lexer
import sifter.extensions.regex  # needed by the lexer
from sifter.grammar import grammar
from sifter.grammar import lexer
from sifter.grammar.command_list import CommandList

__all__ = ('parse_file',)


def parse_file(filehandle: TextIO) -> CommandList:
    return cast(CommandList, grammar.parser().parse(filehandle.read(), lexer=lexer.lexer()))
