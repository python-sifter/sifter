import base

# section 5.8
class SieveTestNot(base.SieveTest):

    RULE_IDENTIFIER = "NOT"

    def __init__(self, arguments=None, tests=None):
        base.SieveTest.__init__(self, arguments, tests)
        self.validate_arguments_size(0)
        self.validate_tests_size(1)

    def evaluate(self, message, state):
        return not self.tests[0].evaluate(message, state)

base.register_sieve_test(SieveTestNot)
