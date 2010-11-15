from sieve.grammar.command import SieveCommand

# section 4.4
class SieveCommandDiscard(SieveCommand):

    RULE_IDENTIFIER = 'DISCARD'

    def __init__(self, arguments=None, tests=None, block=None):
        super(SieveCommandDiscard, self).__init__(arguments, tests, block)
        self.validate_arguments_size(0)
        self.validate_tests_size(0)
        self.validate_block_size(0)

    def evaluate(self, message, state):
        state.actions.cancel_implicit_keep()

SieveCommandDiscard.register()
