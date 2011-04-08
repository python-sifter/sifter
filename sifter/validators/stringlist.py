import sifter.grammar

__all__ = ('StringList',)

class StringList(sifter.grammar.Validator):

    def __init__(self, length=None):
        super(StringList, self).__init__()
        self.length = length

    def validate(self, arg_list, starting_index):
        if starting_index >= len(arg_list):
            return 0
        arg = arg_list[starting_index]

        if not (isinstance(arg, list)
                and all(isinstance(list_member, basestring)
                        for list_member in arg)):
            return 0
        if self.length is not None and len(arg) != self.length:
            return 0

        return 1

