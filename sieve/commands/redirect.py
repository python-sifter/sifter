import email.utils

from sieve.grammar.command import SieveCommand
from sieve.grammar.rule import SieveRuleSyntaxError

# section 4.2
class SieveCommandRedirect(SieveCommand):

    RULE_IDENTIFIER = 'REDIRECT'

    def __init__(self, arguments=None, tests=None, block=None):
        super(SieveCommandRedirect, self).__init__(arguments, tests, block)
        self.validate_arguments_size(1)
        self.validate_tests_size(0)
        self.validate_block_size(0)
        self.validate_arg_is_stringlist(0, 1)
        # TODO: section 2.4.2.3 constrains the email address to a limited
        # subset of valid address formats. need to check if python's
        # email.utils also uses this subset or if we need to do our own
        # parsing.
        realname, emailaddr = email.utils.parseaddr(self.arguments[0][0])
        if emailaddr == "":
            raise SieveRuleSyntaxError(
                    "REDIRECT destination not a valid email address: %s"
                    % self.arguments[0][0]
                    )

    def evaluate(self, message, state):
        state.actions.append('redirect', self.arguments[0][0])
        state.actions.cancel_implicit_keep()

SieveCommandRedirect.register()
