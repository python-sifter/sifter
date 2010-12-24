import sieve.grammar

__all__ = ('SieveCommandDiscard',)

# section 4.4
class SieveCommandDiscard(sieve.grammar.Command):

    RULE_IDENTIFIER = 'DISCARD'

    def __init__(self, arguments=None, tests=None, block=None):
        super(SieveCommandDiscard, self).__init__(arguments, tests, block)
        self.validate_arguments_size(0)
        self.validate_tests_size(0)
        self.validate_block_size(0)

    def evaluate(self, message, state):
        state.actions.cancel_implicit_keep()

SieveCommandDiscard.register()
