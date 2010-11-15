from sieve.grammar.command import SieveCommand

# section 4.3
class SieveCommandKeep(SieveCommand):

    RULE_IDENTIFIER = 'KEEP'

    def __init__(self, arguments=None, tests=None, block=None):
        super(SieveCommandKeep, self).__init__(arguments, tests, block)
        self.validate_arguments_size(0)
        self.validate_tests_size(0)
        self.validate_block_size(0)

    def evaluate(self, message, state):
        state.actions.append('keep').cancel_implicit_keep()

SieveCommandKeep.register()
