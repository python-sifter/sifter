import sifter.grammar

__all__ = ('CommandDiscard',)

# section 4.4
class CommandDiscard(sifter.grammar.Command):

    RULE_IDENTIFIER = 'DISCARD'

    def __init__(self, arguments=None, tests=None, block=None):
        super(CommandDiscard, self).__init__(arguments, tests, block)
        self.validate_arguments()
        self.validate_tests_size(0)
        self.validate_block_size(0)

    def evaluate(self, message, state):
        state.actions.cancel_implicit_keep()

CommandDiscard.register()
