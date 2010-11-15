import sieve.handler

def register(extension_name):
    sieve.handler.register('extension', extension_name, True)
