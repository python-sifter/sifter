from typing import (
    List,
    Optional,
    Text
)

from sifter.grammar.validator import Validator

__all__ = ('StringList',)


class StringList(Validator):

    def __init__(self, length: Optional[int] = None) -> None:
        super(StringList, self).__init__()
        self.length = length

    def validate(self, arg_list: List[Text], starting_index: int) -> int:
        if starting_index >= len(arg_list):
            return 0
        arg = arg_list[starting_index]

        if not (
            isinstance(arg, list) and
            all(isinstance(list_member, (str, bytes)) for list_member in arg)
        ):
            return 0
        if self.length is not None and len(arg) != self.length:
            return 0

        return 1
