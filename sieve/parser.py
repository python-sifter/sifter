import sieve.extensions.builtin
import sieve.extensions.regex
from sieve.grammar import grammar
from sieve.grammar import lexer

__all__ = ('parse_file',)

def parse_file(filehandle):
    return grammar.parser().parse(filehandle.read(), lexer=lexer.lexer())

