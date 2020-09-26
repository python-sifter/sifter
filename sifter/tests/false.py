from sifter.grammar.test import Test

__all__ = ('TestFalse',)


# section 5.6
class TestFalse(Test):

    RULE_IDENTIFIER = 'FALSE'

    def __init__(self, arguments=None, tests=None):
        super(TestFalse, self).__init__(arguments, tests)
        self.validate_arguments()
        self.validate_tests_size(0)

    def evaluate(self, message, state):
        return False


TestFalse.register()
