from typing import (
    TYPE_CHECKING,
    Callable,
    Text,
    Optional,
    Tuple,
    Type,
    Union
)

import sifter.handler

if TYPE_CHECKING:
    from sifter.grammar.comparator import Comparator
    from sifter.grammar.tag import Tag
    from sifter.grammar.state import EvaluationState

__all__ = ('register', 'get_match_fn',)


def register(comparator_name: Optional[Text], comparator_cls: Type['Comparator']) -> None:
    sifter.handler.register('comparator', comparator_name, comparator_cls)


def get_match_fn(comparator: Optional[Union[Text, 'Tag']], match_type: Optional[Union[Text, 'Tag']]) -> Tuple[Callable[[Text, Text, 'EvaluationState'], bool], Union[Text, 'Tag'], Union[Text, 'Tag']]:
    # section 2.7.3: default comparator is 'i;ascii-casemap'
    if comparator is None:
        comparator = 'i;ascii-casemap'
    # RFC 4790, section 3.1: the special identifier 'default' refers to the
    # implementation-defined default comparator
    elif comparator == 'default':
        comparator = 'i;ascii-casemap'

    # section 2.7.1: default match type is ":is"
    if match_type is None:
        match_type = 'IS'

    # TODO: support wildcard matching in comparator names (RFC 4790)
    cmp_handler = sifter.handler.get('comparator', comparator)
    if not cmp_handler:
        raise RuntimeError("Comparator not supported: %s" % comparator)

    try:
        cmp_fn = getattr(cmp_handler, 'cmp_%s' % match_type.lower())
    except AttributeError:
        raise RuntimeError(
            "':%s' matching not supported by comparator '%s'"
            % (match_type, comparator)
        )

    return (cmp_fn, comparator, match_type)
