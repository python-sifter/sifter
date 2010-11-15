from sieve.grammar.test import SieveTest

# section 5.8
class SieveTestNot(SieveTest):

    RULE_IDENTIFIER = 'NOT'

    def __init__(self, arguments=None, tests=None):
        super(SieveTestNot, self).__init__(arguments, tests)
        self.validate_arguments_size(0)
        self.validate_tests_size(1)

    def evaluate(self, message, state):
        return not self.tests[0].evaluate(message, state)

SieveTestNot.register()
