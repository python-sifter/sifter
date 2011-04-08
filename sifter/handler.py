
_HANDLERS_MAP = {}

def register(handler_type, handler_id, value):
    _HANDLERS_MAP.setdefault(handler_type, {})[handler_id] = value

def unregister(handler_type, handler_id):
    return _HANDLERS_MAP.get(handler_type, {}).pop(handler_id, None)

def get(handler_type, handler_id):
    return _HANDLERS_MAP.get(handler_type, {}).get(handler_id, None)

