import sifter.grammar

__all__ = ('CommandKeep',)

# section 4.3
class CommandKeep(sifter.grammar.Command):

    RULE_IDENTIFIER = 'KEEP'

    def __init__(self, arguments=None, tests=None, block=None):
        super(CommandKeep, self).__init__(arguments, tests, block)
        self.validate_arguments()
        self.validate_tests_size(0)
        self.validate_block_size(0)

    def evaluate(self, message, state):
        state.actions.append('keep').cancel_implicit_keep()

CommandKeep.register()
