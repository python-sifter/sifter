from typing import (
    Any,
    Dict,
    Text,
    Optional
)


_HANDLERS_MAP: Dict[Text, Dict[Text, Any]] = {}


def register(handler_type: Optional[Text], handler_id: Optional[Text], value: Any) -> None:
    if not handler_type or not handler_id:
        raise ValueError("handler_type and handler_id must not be None!")
    _HANDLERS_MAP.setdefault(handler_type, {})[handler_id] = value


def unregister(handler_type: Text, handler_id: Text) -> Any:
    return _HANDLERS_MAP.get(handler_type, {}).pop(handler_id, None)


def get(handler_type: Text, handler_id: Text) -> Any:
    return _HANDLERS_MAP.get(handler_type, {}).get(handler_id, None)
