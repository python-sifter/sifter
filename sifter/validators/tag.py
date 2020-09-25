from typing import (
    Union,
    Optional,
    Text,
    List,
    Tuple
)

from sifter.grammar.validator import Validator
from sifter.grammar.rule import RuleSyntaxError
from sifter.grammar import tag
from sifter.validators.stringlist import StringList
import sifter.handler
import sifter.validators

__all__ = ('Tag', 'MatchType', 'Comparator',)


class Tag(Validator):

    def __init__(self, allowed_tags: Optional[Union[Text, bytes, Tuple[Union[Text, bytes], ...]]] = None, tag_arg_validators: Optional[Tuple[Validator, ...]] = None) -> None:
        self.tag_arg_validators: Tuple[Validator, ...]
        super(Tag, self).__init__()
        self.allowed_tags: Optional[Union[Text, bytes, Tuple[Union[Text, bytes], ...]]] = None
        if isinstance(allowed_tags, (str, bytes)):
            self.allowed_tags = (allowed_tags, )
        else:
            self.allowed_tags = allowed_tags
        if tag_arg_validators is None:
            self.tag_arg_validators = ()
        else:
            self.tag_arg_validators = tag_arg_validators

    def validate(self, arg_list: List[tag.Tag], starting_index: int) -> Optional[int]:
        if starting_index >= len(arg_list):
            return 0
        if not isinstance(arg_list[starting_index], tag.Tag):
            return 0

        if self.allowed_tags is not None:
            if arg_list[starting_index] not in self.allowed_tags:
                return 0
        validated_args = 1

        for arg_validator in self.tag_arg_validators:
            num_valid_args = arg_validator.validate(
                arg_list,
                starting_index + validated_args
            )
            if num_valid_args > 0:
                validated_args += num_valid_args
            else:
                return 0

        return validated_args


class MatchType(Tag):

    def __init__(self) -> None:
        super(MatchType, self).__init__(('IS', 'CONTAINS', 'MATCHES'))


class Comparator(Tag):

    def __init__(self) -> None:
        super(Comparator, self).__init__(
            ('COMPARATOR',),
            (StringList(1),),
        )

    def validate(self, arg_list: List[tag.Tag], starting_index: int) -> Optional[int]:
        validated_args = super(Comparator, self).validate(
            arg_list,
            starting_index
        )
        if validated_args and validated_args > 0:
            if not sifter.handler.get(
                'comparator',
                arg_list[starting_index + 1][0],
            ):
                raise RuleSyntaxError(
                    "'%s' comparator is unknown/unsupported"
                    % arg_list[starting_index + 1][0]
                )
        return None
