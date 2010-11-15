from sieve.grammar.command import SieveCommand

# section 3.3
class SieveCommandStop(SieveCommand):

    RULE_IDENTIFIER = 'STOP'

    def __init__(self, arguments=None, tests=None, block=None):
        super(SieveCommandStop, self).__init__(arguments, tests, block)
        self.validate_arguments_size(0)
        self.validate_tests_size(0)
        self.validate_block_size(0)

    def evaluate(self, message, state):
        state.actions.append('stop')

SieveCommandStop.register()
