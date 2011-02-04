import sieve.grammar

__all__ = ('SieveCommandIf', 'SieveCommandElsIf', 'SieveCommandElse',)

# section 3.1
class SieveCommandIfBase(sieve.grammar.Command):

    def __init__(self, arguments=None, tests=None, block=None):
        super(SieveCommandIfBase, self).__init__(arguments, tests, block)
        self.validate_arguments()
        self.validate_tests_size(1)

    def evaluate(self, message, state):
        if self.tests[0].evaluate(message, state):
            result = self.block.evaluate(message, state)
            state.last_if = True
            return result
        else:
            state.last_if = False
            return None


class SieveCommandIf(SieveCommandIfBase):

    RULE_IDENTIFIER = 'IF'

SieveCommandIf.register()


class SieveCommandElsIf(SieveCommandIfBase):

    RULE_IDENTIFIER = 'ELSIF'

    def evaluate(self, message, state):
        if state.last_if:
            return None
        else:
            return super(SieveCommandElsIf, self).evaluate(message, state)

SieveCommandElsIf.register()


class SieveCommandElse(sieve.grammar.Command):

    RULE_IDENTIFIER = 'ELSE'

    def __init__(self, arguments=None, tests=None, block=None):
        super(SieveCommandElse, self).__init__(arguments, tests, block)
        self.validate_arguments()
        self.validate_tests_size(0)

    def evaluate(self, message, state):
        if state.last_if:
            return None
        else:
            return self.block.evaluate(message, state)

SieveCommandElse.register()
