from typing import (
    Any,
    Dict,
    Text
)


_HANDLERS_MAP: Dict[Text, Dict[Text, Any]] = {}


def register(handler_type: Text, handler_id: Text, value: Any) -> None:
    _HANDLERS_MAP.setdefault(handler_type, {})[handler_id] = value


def unregister(handler_type: Text, handler_id: Text) -> Any:
    return _HANDLERS_MAP.get(handler_type, {}).pop(handler_id, None)


def get(handler_type: Text, handler_id: Text) -> Any:
    return _HANDLERS_MAP.get(handler_type, {}).get(handler_id, None)
