import base

# section 5.9
class SieveTestSize(base.SieveTest):

    RULE_IDENTIFIER = "SIZE"

    def __init__(self, arguments=None, tests=None):
        base.SieveTest.__init__(self, arguments, tests)
        self.validate_arguments_size(2)
        self.validate_tests_size(0)
        self.validate_arg_is_tag(0, ("over", "under"))
        self.validate_arg_is_number(1)

    def evaluate(self, message, state):
        # FIXME: size is defined as number of octets, whereas this gives us
        # number of characters
        message_size = len(message.as_string())
        if self.arguments[0] == ":over":
            return message_size > self.arguments[1]
        elif self.arguments[1] == ":under":
            return message_size < self.arguments[1]
