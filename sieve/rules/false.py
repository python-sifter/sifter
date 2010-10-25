from sieve.rules import base

# section 5.6
class SieveTestFalse(base.SieveTest):

    RULE_IDENTIFIER = 'FALSE'

    def __init__(self, arguments=None, tests=None):
        base.SieveTest.__init__(self, arguments, tests)
        self.validate_arguments_size(0)
        self.validate_tests_size(0)

    def evaluate(self, message, state):
        return False
