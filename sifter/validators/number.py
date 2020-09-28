from typing import (
    TYPE_CHECKING,
    List,
    Union,
    Optional,
    SupportsInt,
    Text
)

from sifter.grammar.validator import Validator

if TYPE_CHECKING:
    from sifter.grammar.tag import Tag as TagGrammar
    from sifter.grammar.string import String

__all__ = ('Number',)


class Number(Validator):

    def validate(self, arg_list: List[Union['TagGrammar', SupportsInt, List[Union[Text, 'String']]]], starting_index: int) -> Optional[int]:
        if starting_index >= len(arg_list):
            return 0
        value_to_check = arg_list[starting_index]
        if not isinstance(value_to_check, Text):
            return 0
        try:

            int(value_to_check)
            return 1
        except TypeError:
            return 0
