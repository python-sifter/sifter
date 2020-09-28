from typing import (
    TYPE_CHECKING,
    List,
    Optional,
    Union,
    SupportsInt,
    Text
)

from sifter.grammar.validator import Validator

if TYPE_CHECKING:
    from sifter.grammar.tag import Tag as TagGrammar
    from sifter.grammar.string import String

__all__ = ('StringList',)


class StringList(Validator):

    def __init__(self, length: Optional[int] = None) -> None:
        super(StringList, self).__init__()
        self.length = length

    def validate(
        self,
        arg_list: List[Union['TagGrammar', SupportsInt, List[Union[Text, 'String']]]],
        starting_index: int
    ) -> Optional[int]:
        if starting_index >= len(arg_list):
            return 0
        arg = arg_list[starting_index]

        if not (
            isinstance(arg, list) and
            all(isinstance(list_member, str) for list_member in arg)
        ):
            return 0
        if self.length is not None and len(arg) != self.length:
            return 0

        return 1
