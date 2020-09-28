from typing import (
    TYPE_CHECKING,
    Text,
    Optional,
    List,
    Union
)

if TYPE_CHECKING:
    from sifter.grammar.string import String

__all__ = ('Actions',)


class Actions(list):  # type: ignore

    def __init__(self, implicit_keep: bool = False) -> None:
        super(Actions, self).__init__()
        self.implicit_keep = implicit_keep

    def append(self, action: Text, action_args: Optional[Union[Text, 'String', List[Union[Text, 'String']]]] = None) -> None:
        super(Actions, self).append((action, action_args))

    def cancel_implicit_keep(self) -> 'Actions':
        self.implicit_keep = False
        return self
