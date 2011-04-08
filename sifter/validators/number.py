import sifter.grammar

__all__ = ('Number',)

class Number(sifter.grammar.Validator):

    def validate(self, arg_list, starting_index):
        if starting_index >= len(arg_list):
            return 0
        try:
            long(arg_list[starting_index])
            return 1
        except TypeError:
            return 0

