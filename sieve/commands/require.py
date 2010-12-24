import sieve.grammar
import sieve.handler

__all__ = ('SieveCommandRequire',)

# section 3.2
class SieveCommandRequire(sieve.grammar.Command):

    RULE_IDENTIFIER = 'REQUIRE'

    def __init__(self, arguments=None, tests=None, block=None):
        super(SieveCommandRequire, self).__init__(arguments, tests, block)
        self.validate_arguments_size(1)
        self.validate_tests_size(0)
        self.validate_block_size(0)
        self.validate_arg_is_stringlist(0)

    def evaluate(self, message, state):
        for ext_name in self.arguments[0]:
            if not sieve.handler.get('extension', ext_name):
                raise RuntimeError("Required extension '%s' not supported"
                        % ext_name)
            state.require_extension(ext_name)

SieveCommandRequire.register()
