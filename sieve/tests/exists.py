import sieve.grammar

__all__ = ('SieveTestExists',)

# section 5.9
class SieveTestExists(sieve.grammar.Test):

    RULE_IDENTIFIER = 'EXISTS'

    def __init__(self, arguments=None, tests=None):
        super(SieveTestExists, self).__init__(arguments, tests)
        self.validate_arguments_size(1)
        self.validate_tests_size(0)
        self.validate_arg_is_stringlist(0)

    def evaluate(self, message, state):
        for header in self.arguments[0]:
            if header not in message:
                return False
        return True

SieveTestExists.register()
