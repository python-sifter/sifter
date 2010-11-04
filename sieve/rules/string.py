import sieve.handler

class SieveString(object):

    def __init__(self, s):
        self._s = s

    def __getattr__(self, name):
        return getattr(self._s, name)

def compare(str1, str2, state, comparator=None, match_type=None):
    # section 2.7.3: default comparator is "i;ascii-casemap"
    if comparator is None: comparator = 'i;ascii-casemap'
    # section 2.7.1: default match type is ":is"
    if match_type is None: match_type = 'IS'

    cmp_handler = sieve.handler.get('comparator', comparator)
    if not cmp_handler:
        raise RuntimeError("Comparator not supported: %s" % comparator)
    if ('comparator-%s' % comparator) not in state.required_extensions:
        raise RuntimeError("REQUIRE 'comparator-%s' must happen before "
                           "the comparator can be used." % comparator)

    try:
        return getattr(cmp_handler, match_type.lower())(str1, str2)
    except AttributeError:
        raise RuntimeError(
                "':%s' matching not supported by comparator '%s'"
                % (match_type, comparator)
                )

