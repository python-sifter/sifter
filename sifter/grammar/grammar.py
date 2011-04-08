# Parser based on RFC 5228, especially the grammar as defined in section 8. All
# references are to sections in RFC 5228 unless stated otherwise.

import ply.yacc

import sifter.grammar
from sifter.grammar.lexer import tokens
import sifter.handler

__all__ = ('parser',)


def parser(**kwargs):
    return ply.yacc.yacc(**kwargs)


def p_commands_list(p):
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

def p_commands_empty(p):
    """commands : """
    p[0] = sifter.grammar.CommandList()

def p_command(p):
    """command : IDENTIFIER arguments ';'
               | IDENTIFIER arguments block"""
    #print("COMMAND:", p[1], p[2], p[3])
    tests = p[2].get('tests')
    block = None
    if p[3] != ';': block = p[3]
    handler = sifter.handler.get('command', p[1])
    if handler is None:
        print("No handler registered for command '%s' on line %d" %
            (p[1], p.lineno(1)))
        raise SyntaxError
    p[0] = handler(arguments=p[2]['args'], tests=tests, block=block)

def p_command_error(p):
    """command : IDENTIFIER error ';'
               | IDENTIFIER error block"""
    print("Syntax error in command definition after %s on line %d" %
        (p[1], p.lineno(1)))
    raise SyntaxError

def p_block(p):
    """block : '{' commands '}' """
    # section 3.2: REQUIRE command must come before any other commands,
    # which means it can't be in the block of another command
    if any(command.RULE_IDENTIFIER == 'REQUIRE'
           for command in p[2].commands):
        print("REQUIRE command not allowed inside of a block (line %d)" %
            (p.lineno(2)))
        raise SyntaxError
    p[0] = p[2]

def p_block_error(p):
    """block : '{' error '}'"""
    print("Syntax error in command block that starts on line %d" %
        (p.lineno(1),))
    raise SyntaxError

def p_arguments(p):
    """arguments : argumentlist
                 | argumentlist test
                 | argumentlist '(' testlist ')'"""
    p[0] = { 'args' : p[1], }
    if len(p) > 2:
        if p[2] == '(':
            p[0]['tests'] = p[3]
        else:
            p[0]['tests'] = [ p[2] ]

def p_testlist_error(p):
    """arguments : argumentlist '(' error ')'"""
    print("Syntax error in test list that starts on line %d" % p.lineno(2))
    raise SyntaxError

def p_argumentlist_list(p):
    """argumentlist : argumentlist argument"""
    p[0] = p[1]
    p[0].append(p[2])

def p_argumentlist_empty(p):
    """argumentlist : """
    p[0] = []

def p_test(p):
    """test : IDENTIFIER arguments"""
    #print("TEST:", p[1], p[2])
    tests = p[2].get('tests')
    handler = sifter.handler.get('test', p[1])
    if handler is None:
        print("No handler registered for test '%s' on line %d" %
                (p[1], p.lineno(1)))
        raise SyntaxError
    p[0] = handler(arguments=p[2]['args'], tests=tests)

def p_testlist_list(p):
    """testlist : test ',' testlist"""
    p[0] = p[3]
    p[0].insert(0, p[1])

def p_testlist_single(p):
    """testlist : test"""
    p[0] = [ p[1] ]

def p_argument_stringlist(p):
    """argument : '[' stringlist ']'"""
    p[0] = p[2]

def p_argument_string(p):
    """argument : string"""
    # for simplicity, we treat all single strings as a string list
    p[0] = [ p[1] ]

def p_argument_number(p):
    """argument : NUMBER"""
    p[0] = p[1]

def p_argument_tag(p):
    """argument : TAG"""
    p[0] = sifter.grammar.Tag(p[1])

def p_stringlist_error(p):
    """argument : '[' error ']'"""
    print("Syntax error in string list that starts on line %d" %
            p.lineno(1))
    raise SyntaxError

def p_stringlist_list(p):
    """stringlist : string ',' stringlist"""
    p[0] = p[3]
    p[0].insert(0, p[1])

def p_stringlist_single(p):
    """stringlist : string"""
    p[0] = [ p[1] ]

def p_string(p):
    """string : QUOTED_STRING"""
    p[0] = sifter.grammar.String(p[1])

