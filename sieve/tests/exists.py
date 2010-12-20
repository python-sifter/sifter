import sieve.grammar

__all__ = ('SieveTestExists',)

# section 5.9
class SieveTestExists(sieve.grammar.Test):

    RULE_IDENTIFIER = 'EXISTS'

    def __init__(self, arguments=None, tests=None):
        super(SieveTestExists, self).__init__(arguments, tests)
        tagged_args, positional_args = self.validate_arguments(
                {}, [ validator.StringList(), ])
        self.validate_tests_size(0)
        self.headers = positional_args[0]

    def evaluate(self, message, state):
        for header in self.headers:
            if header not in message:
                return False
        return True

SieveTestExists.register()
