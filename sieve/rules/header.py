from sieve.rules import base
import sieve.rules.string

# section 5.7
class SieveTestHeader(base.SieveTest):

    RULE_IDENTIFIER = 'HEADER'

    def __init__(self, arguments=None, tests=None):
        base.SieveTest.__init__(self, arguments, tests)
        self.validate_arguments_size(2, 5)
        self.validate_tests_size(0)
        self.match_type = self.comparator = None

        headers_idx = len(self.arguments) - 2
        keylist_idx = len(self.arguments) - 1
        if len(self.arguments) == 3:
            self.validate_arg_is_match_type(0)
            self.match_type = self.arguments[0].tag
        elif len(self.arguments) == 4:
            self.validate_arg_is_tag(0, ('COMPARATOR',))
            self.validate_arg_is_comparator(1))
            self.comparator = self.arguments[1]
        elif len(self.arguments) == 5:
            # TODO: allow arguments to come in any order
            self.validate_arg_is_tag(0, ('COMPARATOR',))
            self.validate_arg_is_comparator(1)
            self.comparator = self.arguments[1]
            self.validate_arg_is_match_type(2)
            self.match_type = self.arguments[2].tag

        self.validate_arg_is_stringlist(headers_idx)
        self.validate_arg_is_stringlist(keylist_idx)
        self.headers = self.arguments[headers_idx]
        self.keylist = self.arguments[keylist_idx]

    def evaluate(self, message, state):
        for header in self.headers:
            for value in message.get_all(header, []):
                for key in self.keylist:
                    if sieve.rules.string.compare(value, key, state,
                            self.comparator, self.match_type):
                        return True
        return False
