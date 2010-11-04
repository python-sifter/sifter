from sieve.rules import base

# section 3.1
class SieveCommandIfBase(base.SieveCommand):

    def __init__(self, arguments=None, tests=None, block=None):
        base.SieveCommand.__init__(self, arguments, tests, block)
        self.validate_arguments_size(0)
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


class SieveCommandElsIf(SieveCommandIfBase):

    RULE_IDENTIFIER = 'ELSIF'

    def evaluate(self, message, state):
        if state.last_if:
            return None
        else:
            return SieveCommandIfBase.evaluate(self, message, state)


class SieveCommandElse(base.SieveCommand):

    RULE_IDENTIFIER = 'ELSE'

    def __init__(self, arguments=None, tests=None, block=None):
        base.SieveCommand.__init__(self, arguments, tests, block)
        self.validate_arguments_size(0)
        self.validate_tests_size(0)

    def evaluate(self, message, state):
        if state.last_if:
            return None
        else:
            return self.block.evaluate(message, state)
