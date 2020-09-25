from email.message import Message

from sifter.grammar.command import Command
from sifter.validators.stringlist import StringList
from sifter.grammar.state import EvaluationState


__all__ = ('CommandFileInto',)


# section 4.1
class CommandFileInto(Command):

    RULE_IDENTIFIER = 'FILEINTO'

    def __init__(self, arguments=None, tests=None, block=None) -> None:
        super(CommandFileInto, self).__init__(arguments, tests, block)
        _, positional_args = self.validate_arguments(
            {},
            [StringList(length=1), ],
        )
        self.validate_tests_size(0)
        self.validate_block_size(0)
        self.file_dest = positional_args[0]

    def evaluate(self, message: Message, state: EvaluationState) -> None:
        state.check_required_extension('fileinto', 'FILEINTO')
        state.actions.append('fileinto', self.file_dest)
        state.actions.cancel_implicit_keep()


CommandFileInto.register()
