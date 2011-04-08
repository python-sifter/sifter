import email.utils

import sifter.grammar
import sifter.validators

__all__ = ('CommandRedirect',)

# section 4.2
class CommandRedirect(sifter.grammar.Command):

    RULE_IDENTIFIER = 'REDIRECT'

    def __init__(self, arguments=None, tests=None, block=None):
        super(CommandRedirect, self).__init__(arguments, tests, block)
        _, positional_args = self.validate_arguments(
                {},
                [ sifter.validators.StringList(length=1), ],
            )
        self.validate_tests_size(0)
        self.validate_block_size(0)
        self.email_address = positional_args[0][0]
        # TODO: section 2.4.2.3 constrains the email address to a limited
        # subset of valid address formats. need to check if python's
        # email.utils also uses this subset or if we need to do our own
        # parsing.
        realname, emailaddr = email.utils.parseaddr(self.email_address)
        if emailaddr == "":
            raise sifter.grammar.RuleSyntaxError(
                    "REDIRECT destination not a valid email address: %s"
                    % self.email_address
                    )

    def evaluate(self, message, state):
        state.actions.append('redirect', self.email_address)
        state.actions.cancel_implicit_keep()

CommandRedirect.register()
