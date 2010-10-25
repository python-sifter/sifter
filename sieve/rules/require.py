import base

# section 3.2
class SieveCommandRequire(base.SieveCommand):

    RULE_IDENTIFIER = "REQUIRE"

    def __init__(self, arguments=None, tests=None, block=None):
        base.SieveCommand.__init__(self, arguments, tests, block)
        self.validate_arguments_size(1)
        self.validate_tests_size(0)
        self.validate_block_size(0)
        self.validate_arg_is_stringlist(0)

    def evaluate(self, message, state):
        for extension in self.arguments[0]:
            if not extensions.require(extension):
                raise RuntimeError("Required extension '%s' not supported"
                        % extension)
