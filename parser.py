import math
import ply.lex
import ply.yacc

tokens = ( 'IDENTIFIER', 'NUMBER', 'TAG', 'COMMENT', 'QUOTED_STRING', )
literals = [ c for c in ';,()[]{}' ]

def SieveLexer():
    t_ignore = ' \t'

    def t_COMMENT(t):
        r'\#.*\r\n'
        t.lexer.lineno += 1

    def t_QUOTED_STRING(t):
        r'"([^"\\]|\\["\\])*"'
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

    def t_NUMBER(t):
        r'[0-9]+[KkMmGg]?'
        exponents = {
                "G" : 30, "g" : 30,
                "M" : 20, "m" : 20,
                "K" : 10, "k" : 10,
                }
        if t.value[-1] in exponents:
            t.value = math.ldexp(int(t.value[:-1]), exponents[t.value[-1]])
        else:
            t.value = int(t.value)
        return t

    def t_newline(t):
        r'(\r\n)+'
        t.lexer.lineno += t.value.count("\n")

    return ply.lex.lex()

def SieveParser():
    def p_commands_list(p):
        '''commands : commands command'''
        p[0] = p[1]
        p[0].append(p[2])

    def p_commands_empty(p):
        '''commands : '''
        p[0] = []

    def p_command(p):
        '''command : IDENTIFIER arguments ';'
                   | IDENTIFIER arguments block'''
        p[0] = { 'identifier' : p[1], 'arguments' : p[2], }
        if p[3] != ";":
            p[0]['block'] = p[3]

    def p_command_error(p):
        '''command : IDENTIFIER error ';'
                   | IDENTIFIER error block'''
        print "Syntax error in command definition after %s on line %d" % (p[1], p.lineno(1))

    def p_block(p):
        '''block : '{' commands '}' '''
        p[0] = p[2]

    def p_block_error(p):
        '''block : '{' error '}' '''
        print "Syntax error in command block that starts on line %d" % p.lineno(1)

    def p_arguments(p):
        '''arguments : argumentlist
                     | argumentlist test
                     | argumentlist '(' testlist ')' '''
        p[0] = { 'args' : p[1], }
        if len(p) > 2:
            if p[2] == '(':
                p[0]['tests'] = p[3]
            else:
                p[0]['tests'] = [ p[2] ]

    def p_testlist_error(p):
        '''arguments : argumentlist '(' error ')' '''
        print "Syntax error in test list that starts on line %d" % p.lineno(2)

    def p_argumentlist_list(p):
        '''argumentlist : argumentlist argument'''
        p[0] = p[1]
        p[0].append(p[2])

    def p_argumentlist_empty(p):
        '''argumentlist : '''
        p[0] = []

    def p_test(p):
        '''test : IDENTIFIER arguments'''
        p[0] = { 'identifier' : p[1], 'arguments' : p[2], }

    def p_testlist_list(p):
        '''testlist : test ',' testlist'''
        p[0] = p[3]
        p[0].insert(0, p[1])

    def p_testlist_single(p):
        '''testlist : test'''
        p[0] = [ p[1] ]

    def p_argument_stringlist(p):
        '''argument : '[' stringlist ']' '''
        p[0] = { 'type' : 'LIST', 'value' : p[2], }

    def p_argument_string(p):
        '''argument : string'''
        p[0] = { 'type' : 'STRING', 'value': p[1], }

    def p_argument_number(p):
        '''argument : NUMBER'''
        p[0] = { 'type' : 'NUMBER', 'value': p[1], }

    def p_argument_tag(p):
        '''argument : TAG'''
        p[0] = { 'type' : 'TAG', 'value': p[1], }

    def p_stringlist_error(p):
        '''argument : '[' error ']' '''
        print "Syntax error in string list that starts on line %d" % p.lineno(1)

    def p_stringlist_list(p):
        '''stringlist : string ',' stringlist'''
        p[0] = p[3]
        p[0].insert(0, p[1])

    def p_stringlist_single(p):
        '''stringlist : string'''
        p[0] = [ p[1] ]

    def p_string(p):
        '''string : QUOTED_STRING'''
        p[0] = p[1]

    return ply.yacc.yacc()

