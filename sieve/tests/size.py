from sieve.grammar.test import SieveTest

# section 5.9
class SieveTestSize(SieveTest):

    RULE_IDENTIFIER = 'SIZE'

    def __init__(self, arguments=None, tests=None):
        super(SieveTestSize, self).__init__(arguments, tests)
        self.validate_arguments_size(2)
        self.validate_tests_size(0)
        self.validate_arg_is_tag(0, ('OVER', 'UNDER'))
        self.validate_arg_is_number(1)

    def evaluate(self, message, state):
        # FIXME: size is defined as number of octets, whereas this gives us
        # number of characters
        message_size = len(message.as_string())
        if self.arguments[0].tag == 'OVER':
            return message_size > self.arguments[1]
        elif self.arguments[0].tag == 'UNDER':
            return message_size < self.arguments[1]

SieveTestSize.register()
