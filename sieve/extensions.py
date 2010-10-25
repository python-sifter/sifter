
_EXTENSION_MAP = {}

def register(extension_name):
    _EXTENSION_MAP[extension_name] = False

def require(extension_name):
    if extension_name in _EXTENSION_MAP:
        _EXTENSION_MAP[extension_name] = True
        return True
    else:
        return False

def has_been_required(extension_name):
    return _EXTENSION_MAP.get(extension_name, False)

