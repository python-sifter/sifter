# Parser based on RFC 5228, especially the grammar as defined in section 8. All
# references are to sections in RFC 5228 unless stated otherwise.

from sifter.grammar.test import Test
from sifter.grammar.command import Command
from typing import (
    TYPE_CHECKING,
    Any
)

import ply.yacc  # type: ignore

import sifter.grammar
from sifter.grammar.tag import Tag
from sifter.grammar.lexer import tokens
from sifter.grammar.command_list import CommandList
from sifter.grammar.string import String
import sifter.handler

if TYPE_CHECKING:
    from py.yacc import LRParser, YaccProduction  # type: ignore

__all__ = ('parser',)


def parser(**kwargs: Any) -> 'LRParser':
    return ply.yacc.yacc(**kwargs)


def p_commands_list(p: 'YaccProduction') -> None:
    """commands : commands command"""
    p[0] = p[1]

    # section 3.2: REQUIRE command must come before any other commands
    if p[2].RULE_IDENTIFIER == 'REQUIRE':
        if any(command.RULE_IDENTIFIER != 'REQUIRE'
               for command in p[0].commands):
            print("REQUIRE command on line %d must come before any "
                  "other non-REQUIRE commands" % p.lineno(2))
            raise SyntaxError

    # section 3.1: ELSIF and ELSE must follow IF or another ELSIF
    elif p[2].RULE_IDENTIFIER in ('ELSIF', 'ELSE'):
        if p[0].commands[-1].RULE_IDENTIFIER not in ('IF', 'ELSIF'):
            print("ELSIF/ELSE command on line %d must follow an IF/ELSIF "
                  "command" % p.lineno(2))
            raise SyntaxError

    p[0].commands.append(p[2])


def p_commands_empty(p: 'YaccProduction') -> None:
    """commands : """
    p[0] = CommandList()


def p_command(p: 'YaccProduction') -> None:
    """command : IDENTIFIER arguments ';'
               | IDENTIFIER arguments block"""
    # print("COMMAND:", p[1], p[2], p[3])
    tests = p[2].get('tests')
    block = None
    if p[3] != ';':
        block = p[3]
    handler = sifter.handler.get('command', p[1])
    if handler is None:
        print("No handler registered for command '%s' on line %d" % (p[1], p.lineno(1)))
        raise SyntaxError
    if not isinstance(handler, type) or not issubclass(handler, Command):
        raise ValueError("handler must be subclass of Command")
    p[0] = handler(arguments=p[2]['args'], tests=tests, block=block)


def p_command_error(p: 'YaccProduction') -> None:
    """command : IDENTIFIER error ';'
               | IDENTIFIER error block"""
    print("Syntax error in command definition after %s on line %d" % (p[1], p.lineno(1)))
    raise SyntaxError


def p_block(p: 'YaccProduction') -> None:
    """block : '{' commands '}' """
    # section 3.2: REQUIRE command must come before any other commands,
    # which means it can't be in the block of another command
    if any(command.RULE_IDENTIFIER == 'REQUIRE'
           for command in p[2].commands):
        print("REQUIRE command not allowed inside of a block (line %d)" % (p.lineno(2)))
        raise SyntaxError
    p[0] = p[2]


def p_block_error(p: 'YaccProduction') -> None:
    """block : '{' error '}'"""
    print("Syntax error in command block that starts on line %d" % (p.lineno(1),))
    raise SyntaxError


def p_arguments(p: 'YaccProduction') -> None:
    """arguments : argumentlist
                 | argumentlist test
                 | argumentlist '(' testlist ')'"""
    p[0] = {'args': p[1], }
    if len(p) > 2:
        if p[2] == '(':
            p[0]['tests'] = p[3]
        else:
            p[0]['tests'] = [p[2]]


def p_testlist_error(p: 'YaccProduction') -> None:
    """arguments : argumentlist '(' error ')'"""
    print("Syntax error in test list that starts on line %d" % p.lineno(2))
    raise SyntaxError


def p_argumentlist_list(p: 'YaccProduction') -> None:
    """argumentlist : argumentlist argument"""
    p[0] = p[1]
    p[0].append(p[2])


def p_argumentlist_empty(p: 'YaccProduction') -> None:
    """argumentlist : """
    p[0] = []


def p_test(p: 'YaccProduction') -> None:
    """test : IDENTIFIER arguments"""
    # print("TEST:", p[1], p[2])
    tests = p[2].get('tests')
    handler = sifter.handler.get('test', p[1])
    if handler is None:
        print("No handler registered for test '%s' on line %d" % (p[1], p.lineno(1)))
        raise SyntaxError
    if not isinstance(handler, type) or not issubclass(handler, Test):
        raise ValueError("handler must be subclass of Test")
    p[0] = handler(arguments=p[2]['args'], tests=tests)


def p_testlist_list(p: 'YaccProduction') -> None:
    """testlist : test ',' testlist"""
    p[0] = p[3]
    p[0].insert(0, p[1])


def p_testlist_single(p: 'YaccProduction') -> None:
    """testlist : test"""
    p[0] = [p[1]]


def p_argument_stringlist(p: 'YaccProduction') -> None:
    """argument : '[' stringlist ']'"""
    p[0] = p[2]


def p_argument_string(p: 'YaccProduction') -> None:
    """argument : string"""
    # for simplicity, we treat all single strings as a string list
    p[0] = [p[1]]


def p_argument_number(p: 'YaccProduction') -> None:
    """argument : NUMBER"""
    p[0] = p[1]


def p_argument_tag(p: 'YaccProduction') -> None:
    """argument : TAG"""
    p[0] = Tag(p[1])


def p_stringlist_error(p: 'YaccProduction') -> None:
    """argument : '[' error ']'"""
    print("Syntax error in string list that starts on line %d" % p.lineno(1))
    raise SyntaxError


def p_stringlist_list(p: 'YaccProduction') -> None:
    """stringlist : string ',' stringlist"""
    p[0] = p[3]
    p[0].insert(0, p[1])


def p_stringlist_single(p: 'YaccProduction') -> None:
    """stringlist : string"""
    p[0] = [p[1]]


def p_string(p: 'YaccProduction') -> None:
    """string : QUOTED_STRING"""
    p[0] = String(p[1])
