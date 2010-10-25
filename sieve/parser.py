import math
import ply.lex
import ply.yacc

import rules.base

# Parser based on RFC 5228, especially the grammar as defined in section 8. All
# references are to sections in RFC 5228 unless stated otherwise.

tokens = (
    'IDENTIFIER', 'NUMBER', 'TAG', 'HASH_COMMENT', 'BRACKET_COMMENT',
    'QUOTED_STRING', 'MULTILINE_STRING',
    )
literals = [ c for c in ';,()[]{}' ]

def SieveLexer():

    # section 2.2
    t_ignore = ' \t'

    # section 2.3
    def t_HASH_COMMENT(t):
        r'\#.*\r\n'
        t.lexer.lineno += 1

    # section 2.3
    def t_BRACKET_COMMENT(t):
        r'/\*.*\*/'
        # TODO: Bracketed comments begin with the token "/*" and end with "*/"
        # outside of a string.  Bracketed comments may span multiple lines.
        # Bracketed comments do not nest.
        pass

    # section 2.4.2
    def t_MULTILINE_STRING(t):
        r'"@@@@@@@@@@@@@@@"'
        # TODO: For entering larger amounts of text, such as an email message,
        # a multi-line form is allowed.  It starts with the keyword "text:",
        # followed by a CRLF, and ends with the sequence of a CRLF, a single
        # period, and another CRLF.  The CRLF before the final period is
        # considered part of the value.  In order to allow the message to
        # contain lines with a single dot, lines are dot-stuffed.  That is,
        # when composing a message body, an extra '.' is added before each line
        # that begins with a '.'.  When the server interprets the script, these
        # extra dots are removed.  Note that a line that begins with a dot
        # followed by a non-dot character is not interpreted as dot-stuffed;
        # that is, ".foo" is interpreted as ".foo".  However, because this is
        # potentially ambiguous, scripts SHOULD be properly dot-stuffed so such
        # lines do not appear.
        pass

    # section 2.4.2
    def t_QUOTED_STRING(t):
        r'"([^"\\]|\\["\\])*"'
        # TODO: Add support for:
        # - An undefined escape sequence (such as "\a" in a context where "a"
        # has no special meaning) is interpreted as if there were no backslash
        # (in this case, "\a" is just "a"), though that may be changed by
        # extensions.
        # - Non-printing characters such as tabs, CRLF, and control characters
        # are permitted in quoted strings.  Quoted strings MAY span multiple
        # lines.  An unencoded NUL (US-ASCII 0) is not allowed in strings.
        t.value = t.value.strip('"').replace(r'\"', '"').replace(r'\\', '\\')
        return t

    def t_TAG(t):
        r':[a-zA-Z_][a-zA-Z0-9_]*'
        t.value = t.value[1:].upper()
        return t

    def t_IDENTIFIER(t):
        r'[a-zA-Z_][a-zA-Z0-9_]*'
        t.value = t.value.upper()
        return t

    # section 2.4.1
    def t_NUMBER(t):
        r'[0-9]+[KkMmGg]?'
        exponents = {
                'G' : 30, 'g' : 30,
                'M' : 20, 'm' : 20,
                'K' : 10, 'k' : 10,
                }
        if t.value[-1] in exponents:
            t.value = math.ldexp(int(t.value[:-1]), exponents[t.value[-1]])
        else:
            t.value = int(t.value)
        return t

    def t_newline(t):
        r'(\r\n)+'
        t.lexer.lineno += t.value.count('\n')

    return ply.lex.lex()


def SieveParser():

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
        p[0] = rules.base.SieveCommandList()

    def p_command(p):
        """command : IDENTIFIER arguments ';'
                   | IDENTIFIER arguments block"""
        #print("COMMAND:", p[1], p[2], p[3])
        tests = p[2].get('tests')
        block = None
        if p[3] != ';': block = p[3]
        handler = rules.base.SieveCommand.get_rule_handler(p[1])
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
        handler = rules.base.SieveTest.get_rule_handler(p[1])
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
        p[0] = rules.base.SieveTag(p[1])

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
        p[0] = p[1]

    return ply.yacc.yacc()


def parse_file(filehandle):
    import extensions.builtin
    rules.base.SieveCommand.register_imported_rules()
    rules.base.SieveTest.register_imported_rules()

    return SieveParser().parse(filehandle.read(), lexer=SieveLexer())

