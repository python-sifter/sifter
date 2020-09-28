from typing import (
    TYPE_CHECKING,
    Dict,
    Text,
    Optional,
    Union,
    Type
)

if TYPE_CHECKING:
    from sifter.grammar.comparator import Comparator
    from sifter.grammar.rule import Rule


_HANDLERS_MAP: Dict[Text, Dict[Text, Union[bool, Type['Comparator'], Type['Rule']]]] = {}


def register(
    handler_type: Optional[Text],
    handler_id: Optional[Text],
    value: Union[bool, Type['Comparator'], Type['Rule']]
) -> None:
    if not handler_type or not handler_id:
        raise ValueError("handler_type and handler_id must not be None!")
    _HANDLERS_MAP.setdefault(handler_type, {})[handler_id] = value


def unregister(handler_type: Text, handler_id: Text) -> Optional[Union[bool, Type['Comparator'], Type['Rule']]]:
    return _HANDLERS_MAP.get(handler_type, {}).pop(handler_id, None)


def get(handler_type: Text, handler_id: Text) -> Optional[Union[bool, Type['Comparator'], Type['Rule']]]:
    return _HANDLERS_MAP.get(handler_type, {}).get(handler_id, None)
