import email.utils
from email.message import Message
from typing import (
    TYPE_CHECKING,
    List,
    Optional,
    Union,
    SupportsInt,
    Text
)

from sifter.grammar.command import Command
from sifter.grammar.command_list import CommandList
from sifter.grammar.rule import RuleSyntaxError
from sifter.validators.stringlist import StringList
from sifter.grammar.state import EvaluationState
from sifter.grammar.actions import Actions

if TYPE_CHECKING:
    from sifter.grammar.tag import Tag as TagGrammar
    from sifter.grammar.string import String
    from sifter.grammar.test import Test

__all__ = ('CommandRedirect',)


# section 4.2
class CommandRedirect(Command):

    RULE_IDENTIFIER = 'REDIRECT'

    def __init__(
        self,
        arguments: Optional[List[Union['TagGrammar', SupportsInt, List[Union[Text, 'String']]]]] = None,
        tests: Optional[List['Test']] = None,
        block: Optional[CommandList] = None
    ) -> None:
        super(CommandRedirect, self).__init__(arguments, tests, block)
        _, positional_args = self.validate_arguments(
            {},
            [StringList(length=1), ],
        )
        self.validate_tests_size(0)
        self.validate_block_size(0)
        if not isinstance(positional_args, list):
            raise ValueError("CommandRedirect positional argument error")
        if not isinstance(positional_args[0], list):
            raise ValueError("CommandRedirect positional argument error")
        self.email_address = positional_args[0][0]
        # TODO: section 2.4.2.3 constrains the email address to a limited
        # subset of valid address formats. need to check if python's
        # email.utils also uses this subset or if we need to do our own
        # parsing.
        realname, emailaddr = email.utils.parseaddr(self.email_address)
        if emailaddr == "":
            raise RuleSyntaxError(
                "REDIRECT destination not a valid email address: %s"
                % self.email_address
            )

    def evaluate(self, message: Message, state: EvaluationState) -> Optional[Actions]:
        state.actions.append('redirect', self.email_address)
        state.actions.cancel_implicit_keep()
        return None


CommandRedirect.register()
