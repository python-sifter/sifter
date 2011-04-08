import sifter.grammar

__all__ = ('CommandStop',)

# section 3.3
class CommandStop(sifter.grammar.Command):

    RULE_IDENTIFIER = 'STOP'

    def __init__(self, arguments=None, tests=None, block=None):
        super(CommandStop, self).__init__(arguments, tests, block)
        self.validate_arguments()
        self.validate_tests_size(0)
        self.validate_block_size(0)

    def evaluate(self, message, state):
        state.actions.append('stop')

CommandStop.register()
