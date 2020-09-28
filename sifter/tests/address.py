from email.message import Message
import email.utils
from typing import (
    TYPE_CHECKING,
    cast,
    Text,
    List,
    Optional,
    Union,
    SupportsInt
)

from sifter.validators.tag import Tag, Comparator, MatchType
import sifter.grammar
from sifter.grammar.test import Test
import sifter.grammar.string
from sifter.validators.stringlist import StringList
from sifter.grammar.state import EvaluationState

if TYPE_CHECKING:
    from sifter.grammar.tag import Tag as TagGrammar
    from sifter.grammar.string import String

__all__ = ('TestAddress',)


# section 5.1
class TestAddress(Test):

    RULE_IDENTIFIER: Text = 'ADDRESS'

    def __init__(
        self,
        arguments: Optional[List[Union['TagGrammar', SupportsInt, List[Union[Text, 'String']]]]] = None,
        tests: Optional[List['Test']] = None
    ) -> None:
        super(TestAddress, self).__init__(arguments, tests)
        tagged_args, positional_args = self.validate_arguments(
            {
                'comparator': Comparator(),
                'match_type': MatchType(),
                'address_part': Tag(('LOCALPART', 'DOMAIN', 'ALL')),
            },
            [
                StringList(),
                StringList(),
            ]
        )
        self.validate_tests_size(0)

        self.headers, self.keylist = positional_args
        self.match_type = self.comparator = self.address_part = None
        if 'comparator' in tagged_args:
            self.comparator = tagged_args['comparator'][1][0]  # type: ignore
        if 'match_type' in tagged_args:
            self.match_type = tagged_args['match_type'][0]
        if 'address_part' in tagged_args:
            self.address_part = tagged_args['address_part'][0]

    def evaluate(self, message: Message, state: EvaluationState) -> Optional[bool]:
        if not isinstance(self.keylist, list):
            raise ValueError('TestAddress keylist not iterable')

        if not isinstance(self.headers, list):
            raise ValueError('TestAddress headers not iterable')

        header_values: List[Text] = []
        for header in self.headers:
            # TODO: section 5.1: we should restrict the allowed headers to
            # those headers that contain an "address-list". this includes at
            # least: from, to, cc, bcc, sender, resent-from, resent-to.
            header_values.extend(message.get_all(header, []))
        addresses: List[Text] = []
        for msg_address in email.utils.getaddresses(header_values):
            if msg_address[1] != '':
                addresses.append(
                    sifter.grammar.string.address_part(
                        msg_address[1],
                        cast(Text, self.address_part)
                    )
                )
        for address in addresses:
            for key in self.keylist:
                if sifter.grammar.string.compare(
                    address,
                    key,
                    state,
                    self.comparator,
                    cast(Text, self.match_type)
                ):
                    return True
        return False


TestAddress.register()
