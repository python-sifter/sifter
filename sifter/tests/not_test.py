import sifter.grammar

__all__ = ('TestNot',)

# section 5.8
class TestNot(sifter.grammar.Test):

    RULE_IDENTIFIER = 'NOT'

    def __init__(self, arguments=None, tests=None):
        super(TestNot, self).__init__(arguments, tests)
        self.validate_arguments()
        self.validate_tests_size(1)

    def evaluate(self, message, state):
        return not self.tests[0].evaluate(message, state)

TestNot.register()
