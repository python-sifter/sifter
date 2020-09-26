from typing import List

from sifter.grammar.validator import Validator

__all__ = ('Number',)


class Number(Validator):

    def validate(self, arg_list: List[int], starting_index: int) -> int:
        if starting_index >= len(arg_list):
            return 0
        try:
            int(arg_list[starting_index])
            return 1
        except TypeError:
            return 0
