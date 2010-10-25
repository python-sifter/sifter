import base

# section 5.10
class SieveTestTrue(base.SieveTest):

    RULE_IDENTIFIER = "TRUE"

    def __init__(self, arguments=None, tests=None):
        base.SieveTest.__init__(self, arguments, tests)
        self.validate_arguments_size(0)
        self.validate_tests_size(0)

    def evaluate(self, message, state):
        return True

base.register_sieve_test(SieveTestTrue)
