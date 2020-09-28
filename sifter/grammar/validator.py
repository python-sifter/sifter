from typing import (
    TYPE_CHECKING,
    List,
    Optional,
    Union,
    SupportsInt,
    Text
)

if TYPE_CHECKING:
    from sifter.grammar.tag import Tag as TagGrammar
    from sifter.grammar.string import String

__all__ = ('Validator',)


class Validator(object):

    def validate(
        self,
        arg_list: List[Union['TagGrammar', SupportsInt, List[Union[Text, 'String']]]],
        starting_index: int
    ) -> Optional[int]:
        raise NotImplementedError
