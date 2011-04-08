import sifter.grammar
import sifter.grammar.string
import sifter.validators

__all__ = ('TestHeader',)

# section 5.7
class TestHeader(sifter.grammar.Test):

    RULE_IDENTIFIER = 'HEADER'

    def __init__(self, arguments=None, tests=None):
        super(TestHeader, self).__init__(arguments, tests)
        tagged_args, positional_args = self.validate_arguments(
                {
                    'comparator' : sifter.validators.Comparator(),
                    'match_type' : sifter.validators.MatchType(),
                },
                [
                    sifter.validators.StringList(),
                    sifter.validators.StringList(),
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
                    if sifter.grammar.string.compare(value, key, state,
                            self.comparator, self.match_type):
                        return True
        return False

TestHeader.register()
