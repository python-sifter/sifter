from sieve.grammar.command_list import SieveCommandList
from sieve.grammar.rule import SieveRule, SieveRuleSyntaxError
import sieve.utils


class SieveCommand(SieveRule):

    RULE_TYPE = 'command'

    def __init__(self, arguments=None, tests=None, block=None):
        super(SieveCommand, self).__init__(arguments, tests)
        if block is None:
            self.block = SieveCommandList()
        else:
            self.block = block

    def __str__(self):
        s = [ super(SieveCommand, self).__str__(), ]
        if len(self.block.commands) > 0:
            s.append("{\n")
            for command in self.block.commands:
                s.append(sieve.utils.indent_string(str(command), 2))
            s.append("}\n")
        return ''.join(s)

    def validate_block_size(self, max_commands):
        if len(self.block.commands) > max_commands:
            raise SieveRuleSyntaxError("%s takes no more than %d commands" % (
                self.RULE_IDENTIFIER, max_commands))

