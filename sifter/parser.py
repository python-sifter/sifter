import sifter.extensions.builtin  # needed by the lexer
import sifter.extensions.regex  # needed by the lexer
from sifter.grammar import grammar
from sifter.grammar import lexer

__all__ = ('parse_file',)


def parse_file(filehandle):
    return grammar.parser().parse(filehandle.read(), lexer=lexer.lexer())
