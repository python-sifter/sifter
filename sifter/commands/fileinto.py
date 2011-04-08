import sifter.grammar
import sifter.validators

__all__ = ('CommandFileInto',)

# section 4.1
class CommandFileInto(sifter.grammar.Command):

    RULE_IDENTIFIER = 'FILEINTO'

    def __init__(self, arguments=None, tests=None, block=None):
        super(CommandFileInto, self).__init__(arguments, tests, block)
        _, positional_args = self.validate_arguments(
                {},
                [ sifter.validators.StringList(length=1), ],
            )
        self.validate_tests_size(0)
        self.validate_block_size(0)
        self.file_dest = positional_args[0]

    def evaluate(self, message, state):
        state.check_required_extension('fileinto', 'FILEINTO')
        state.actions.append('fileinto', self.file_dest)
        state.actions.cancel_implicit_keep()

CommandFileInto.register()
