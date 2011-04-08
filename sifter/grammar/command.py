import sifter.grammar
import rule
import sifter.utils

__all__ = ('Command',)

class Command(rule.Rule):

    RULE_TYPE = 'command'

    def __init__(self, arguments=None, tests=None, block=None):
        super(Command, self).__init__(arguments, tests)
        if block is None:
            self.block = sifter.grammar.CommandList()
        else:
            self.block = block

    def __str__(self):
        s = [ super(Command, self).__str__(), ]
        if len(self.block.commands) > 0:
            s.append("{\n")
            for command in self.block.commands:
                s.append(sifter.utils.indent_string(str(command), 2))
            s.append("}\n")
        return ''.join(s)

    def validate_block_size(self, max_commands):
        if len(self.block.commands) > max_commands:
            raise sifter.grammar.RuleSyntaxError("%s takes no more than %d commands" % (
                self.RULE_IDENTIFIER, max_commands))

