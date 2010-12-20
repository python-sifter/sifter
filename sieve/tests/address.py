import email.utils

import sieve.grammar
import sieve.grammar.string
import sieve.validators

__all__ = ('SieveTestAddress',)

# section 5.1
class SieveTestAddress(sieve.grammar.Test):

    RULE_IDENTIFIER = 'ADDRESS'

    def __init__(self, arguments=None, tests=None):
        super(SieveTestAddress, self).__init__(arguments, tests)
        tagged_args, positional_args = self.validate_arguments(
                {
                    'comparator' : sieve.validators.Comparator(),
                    'match_type' : sieve.validators.MatchType(),
                    'address_part' : sieve.validators.Tag(
                                        ('LOCALPART', 'DOMAIN', 'ALL')),
                },
                [
                    sieve.validators.StringList(),
                    sieve.validators.StringList(),
                ]
            )
        self.validate_tests_size(0)

        self.headers, self.keylist = positional_args
        self.match_type = self.comparator = self.address_part = None
        if 'comparator' in tagged_args:
            self.comparator = tagged_args['comparator'][1]
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
                addresses.append(sieve.grammar.string.address_part(address[1],
                    self.address_part))
        for address in addresses:
            for key in self.keylist:
                if sieve.grammar.string.compare(address, key, state,
                        self.comparator, self.match_type):
                    return True
        return False

SieveTestAddress.register()
