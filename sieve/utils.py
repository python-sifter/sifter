__all__ = ('indent_string',)

def indent_string(s, num_spaces):
    add_newline = False
    if s[-1] == '\n':
        add_newline = True
        s = s[:-1]
    s = '\n'.join(num_spaces * ' ' + line for line in s.split('\n'))
    if add_newline: s += '\n'
    return s

