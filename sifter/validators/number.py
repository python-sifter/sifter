from typing import List

import sifter.grammar

__all__ = ('Number',)


class Number(sifter.grammar.Validator):

    def validate(self, arg_list: List[int], starting_index: int) -> int:
        if starting_index >= len(arg_list):
            return 0
        try:
            int(arg_list[starting_index])
            return 1
        except TypeError:
            return 0
