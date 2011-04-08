import sifter.grammar

__all__ = ('TestTrue',)

# section 5.10
class TestTrue(sifter.grammar.Test):

    RULE_IDENTIFIER = 'TRUE'

    def __init__(self, arguments=None, tests=None):
        super(TestTrue, self).__init__(arguments, tests)
        self.validate_arguments()
        self.validate_tests_size(0)

    def evaluate(self, message, state):
        return True

TestTrue.register()
