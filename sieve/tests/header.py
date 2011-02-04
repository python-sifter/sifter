import sieve.grammar
import sieve.grammar.string
import sieve.validators

__all__ = ('SieveTestHeader',)

# section 5.7
class SieveTestHeader(sieve.grammar.Test):

    RULE_IDENTIFIER = 'HEADER'

    def __init__(self, arguments=None, tests=None):
        super(SieveTestHeader, self).__init__(arguments, tests)
        tagged_args, positional_args = self.validate_arguments(
                {
                    'comparator' : sieve.validators.Comparator(),
                    'match_type' : sieve.validators.MatchType(),
                },
                [
                    sieve.validators.StringList(),
                    sieve.validators.StringList(),
                ]
            )
        self.validate_tests_size(0)

        self.headers = positional_args[0]
        self.keylist = positional_args[1]
        self.match_type = self.comparator = None
        if 'comparator' in tagged_args:
            self.comparator = tagged_args['comparator'][1][0]
        if 'match_type' in tagged_args:
            self.match_type = tagged_args['match_type'][0]

    def evaluate(self, message, state):
        for header in self.headers:
            for value in message.get_all(header, []):
                for key in self.keylist:
                    if sieve.grammar.string.compare(value, key, state,
                            self.comparator, self.match_type):
                        return True
        return False

SieveTestHeader.register()
