import email.utils

import sifter.grammar
import sifter.grammar.string
import sifter.validators

__all__ = ('TestAddress',)

# section 5.1
class TestAddress(sifter.grammar.Test):

    RULE_IDENTIFIER = 'ADDRESS'

    def __init__(self, arguments=None, tests=None):
        super(TestAddress, self).__init__(arguments, tests)
        tagged_args, positional_args = self.validate_arguments(
                {
                    'comparator' : sifter.validators.Comparator(),
                    'match_type' : sifter.validators.MatchType(),
                    'address_part' : sifter.validators.Tag(
                                        ('LOCALPART', 'DOMAIN', 'ALL')),
                },
                [
                    sifter.validators.StringList(),
                    sifter.validators.StringList(),
                ]
            )
        self.validate_tests_size(0)

        self.headers, self.keylist = positional_args
        self.match_type = self.comparator = self.address_part = None
        if 'comparator' in tagged_args:
            self.comparator = tagged_args['comparator'][1][0]
        if 'match_type' in tagged_args:
            self.match_type = tagged_args['match_type'][0]
        if 'address_part' in tagged_args:
            self.address_part = tagged_args['address_part'][0]

    def evaluate(self, message, state):
        header_values = []
        for header in self.headers:
            # TODO: section 5.1: we should restrict the allowed headers to
            # those headers that contain an "address-list". this includes at
            # least: from, to, cc, bcc, sender, resent-from, resent-to.
            header_values.extend(message.get_all(header, []))
        addresses = []
        for address in email.utils.getaddresses(header_values):
            if address[1] != '':
                addresses.append(sifter.grammar.string.address_part(address[1],
                    self.address_part))
        for address in addresses:
            for key in self.keylist:
                if sifter.grammar.string.compare(address, key, state,
                        self.comparator, self.match_type):
                    return True
        return False

TestAddress.register()
