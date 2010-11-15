from sieve.grammar.test import SieveTest

# section 5.10
class SieveTestTrue(SieveTest):

    RULE_IDENTIFIER = 'TRUE'

    def __init__(self, arguments=None, tests=None):
        super(SieveTestTrue, self).__init__(arguments, tests)
        self.validate_arguments_size(0)
        self.validate_tests_size(0)

    def evaluate(self, message, state):
        return True

SieveTestTrue.register()
