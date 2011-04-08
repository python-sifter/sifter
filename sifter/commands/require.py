import sifter.grammar
import sifter.handler
import sifter.validators

__all__ = ('CommandRequire',)

# section 3.2
class CommandRequire(sifter.grammar.Command):

    RULE_IDENTIFIER = 'REQUIRE'

    def __init__(self, arguments=None, tests=None, block=None):
        super(CommandRequire, self).__init__(arguments, tests, block)
        _, positional_args = self.validate_arguments(
                {},
                [ sifter.validators.StringList(), ],
            )
        self.validate_tests_size(0)
        self.validate_block_size(0)
        self.ext_names = positional_args[0]

    def evaluate(self, message, state):
        for ext_name in self.ext_names:
            if not sifter.handler.get('extension', ext_name):
                raise RuntimeError("Required extension '%s' not supported"
                        % ext_name)
            state.require_extension(ext_name)

CommandRequire.register()
