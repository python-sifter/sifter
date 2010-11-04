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
        cmp_fn = getattr(cmp_handler, 'cmp_%s' % match_type.lower())
    except AttributeError:
        raise RuntimeError(
                "':%s' matching not supported by comparator '%s'"
                % (match_type, comparator)
                )
    return cmp_fn(str1, str2)

def address_part(address, part=None):
    # section 2.7.4: default address part is ":all"
    if part is None: part = 'ALL'

    if part == 'ALL': return address
    try:
        localpart, domain = address.rsplit('@', 1)
    except ValueError:
        # if there's no '@' in the address then treat the whole address as the
        # local part
        localpart = address
        domain = ''
    if part == 'LOCALPART': return localpart
    elif part == 'DOMAIN': return domain
    raise RuntimeError("Unknown address part specified: %s" % part)

