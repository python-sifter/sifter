import sieve.handler

__all__ = ('register',)

def register(extension_name):
    sieve.handler.register('extension', extension_name, True)
