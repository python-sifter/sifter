from typing import Text

import sifter.handler

__all__ = ('register',)


def register(extension_name: Text) -> None:
    sifter.handler.register('extension', extension_name, True)
