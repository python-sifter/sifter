import sifter.handler

__all__ = ('register',)

def register(extension_name):
    sifter.handler.register('extension', extension_name, True)
