import sieve.comparator

__all__ = ('String', 'compare', 'address_part',)


# TODO: this is here because it'll be needed when support for encoded
# characters and variables is added. for now it's just a wrapper around str.
class String(str):

    pass

def compare(str1, str2, state, comparator=None, match_type=None):
    cmp_fn = sieve.comparator.get_match_fn(comparator, match_type)
    if ('comparator-%s' % comparator) not in state.required_extensions:
        raise RuntimeError("REQUIRE 'comparator-%s' must happen before "
                           "the comparator can be used." % comparator)
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

