import base
import extensions

# section 4.1
class SieveCommandFileInto(base.SieveCommand):

    RULE_IDENTIFIER = 'FILEINTO'

    def __init__(self, arguments=None, tests=None, block=None):
        base.SieveCommand.__init__(self, arguments, tests, block)
        self.validate_arguments_size(1)
        self.validate_tests_size(0)
        self.validate_block_size(0)
        self.validate_arg_is_stringlist(0, 1)

    def evaluate(self, message, state):
        if not extensions.has_been_required('fileinto'):
            raise RuntimeError("REQUIRE 'fileinto' must happen before "
                               "FILEINTO can be used.")
        state['actions'].append('fileinto', self.arguments[0][0])
        state['actions'].cancel_implicit_keep()
