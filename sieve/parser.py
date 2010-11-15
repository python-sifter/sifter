from sieve.grammar import grammar
from sieve.grammar import lexer

def parse_file(filehandle):
    import sieve.extensions.builtin
    return grammar.parser().parse(filehandle.read(), lexer=lexer.lexer())

