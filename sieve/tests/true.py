import sieve.grammar

__all__ = ('SieveTestRule',)

# section 5.10
class SieveTestTrue(sieve.grammar.Test):

    RULE_IDENTIFIER = 'TRUE'

    def __init__(self, arguments=None, tests=None):
        super(SieveTestTrue, self).__init__(arguments, tests)
        self.validate_arguments()
        self.validate_tests_size(0)

    def evaluate(self, message, state):
        return True

SieveTestTrue.register()
