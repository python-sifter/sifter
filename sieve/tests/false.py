from sieve.grammar.test import SieveTest

# section 5.6
class SieveTestFalse(SieveTest):

    RULE_IDENTIFIER = 'FALSE'

    def __init__(self, arguments=None, tests=None):
        super(SieveTestFalse, self).__init__(arguments, tests)
        self.validate_arguments_size(0)
        self.validate_tests_size(0)

    def evaluate(self, message, state):
        return False

SieveTestFalse.register()
