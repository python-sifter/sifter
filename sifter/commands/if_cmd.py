import sifter.grammar

__all__ = ('CommandIf', 'CommandElsIf', 'CommandElse',)

# section 3.1
class CommandIfBase(sifter.grammar.Command):

    def __init__(self, arguments=None, tests=None, block=None):
        super(CommandIfBase, self).__init__(arguments, tests, block)
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


class CommandIf(CommandIfBase):

    RULE_IDENTIFIER = 'IF'

CommandIf.register()


class CommandElsIf(CommandIfBase):

    RULE_IDENTIFIER = 'ELSIF'

    def evaluate(self, message, state):
        if state.last_if:
            return None
        else:
            return super(CommandElsIf, self).evaluate(message, state)

CommandElsIf.register()


class CommandElse(sifter.grammar.Command):

    RULE_IDENTIFIER = 'ELSE'

    def __init__(self, arguments=None, tests=None, block=None):
        super(CommandElse, self).__init__(arguments, tests, block)
        self.validate_arguments()
        self.validate_tests_size(0)

    def evaluate(self, message, state):
        if state.last_if:
            return None
        else:
            return self.block.evaluate(message, state)

CommandElse.register()
