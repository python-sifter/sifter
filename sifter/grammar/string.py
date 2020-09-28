from typing import (
    TYPE_CHECKING,
    Text,
    Optional,
    Union
)
import sifter.comparator
from sifter.grammar.state import EvaluationState

if TYPE_CHECKING:
    from sifter.grammar.tag import Tag

__all__ = ('String', 'compare', 'address_part',)


# TODO: this is here because it'll be needed when support for encoded
# characters and variables is added. for now it's just a wrapper around str.
class String(str):
    pass


def compare(str1: Text, str2: Text, state: EvaluationState, comparator: Optional[Union[Text, 'Tag']] = None, match_type: Optional[Union[Text, 'Tag']] = None) -> bool:
    cmp_fn, comparator, match_type = sifter.comparator.get_match_fn(comparator, match_type)
    state.check_required_extension('comparator-%s' % comparator, 'the comparator')
    return cmp_fn(str1, str2, state)


def address_part(address: Text, part: Optional[Text] = None) -> Text:
    # section 2.7.4: default address part is ":all"
    if part is None:
        part = 'ALL'

    if part == 'ALL':
        return address
    try:
        localpart, domain = address.rsplit('@', 1)
    except ValueError:
        # if there's no '@' in the address then treat the whole address as the
        # local part
        localpart = address
        domain = ''
    if part == 'LOCALPART':
        return localpart
    if part == 'DOMAIN':
        return domain
    raise RuntimeError("Unknown address part specified: %s" % part)
