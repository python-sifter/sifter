
_EXTENSION_MAP = {}
def register_sieve_extension(extension_name):
    _EXTENSION_MAP[extension_name] = True
def check_sieve_extension(extension_name):
    return extension_name in _EXTENSION_MAP

_COMMAND_MAP = {}
def register_sieve_command(command):
    _COMMAND_MAP[command.RULE_IDENTIFIER] = command
def get_sieve_command_handler(command_name):
    return _COMMAND_MAP.get(command_name)

_TEST_MAP = {}
def register_sieve_test(test):
    _TEST_MAP[test.RULE_IDENTIFIER] = test
def get_sieve_test_handler(test_name):
    return _TEST_MAP.get(test_name)


def indent_string(s, num_spaces):
    add_newline = False
    if s[-1] == "\n":
        add_newline = True
        s = s[:-1]
    s = "\n".join(num_spaces * " " + line for line in s.split("\n"))
    if add_newline: s += "\n"
    return s


class SieveRuleSyntaxError(Exception):
    pass


class SieveRule(object):

    def __init__(self, arguments=None, tests=None):
        if arguments is None:
            self.arguments = []
        else:
            self.arguments = arguments
        if tests is None:
            self.tests = []
        else:
            self.tests = tests

    def __str__(self):
        s = "%s" % self.RULE_IDENTIFIER
        for arg in self.arguments:
            s += " %s" % arg
        s += "\n"
        for test in self.tests:
            s += "(\n%s)\n" % indent_string(str(test), 2)
        return s

    def validate_arguments_size(self, min_args, max_args=None):
        if max_args is None:
            max_args = min_args
        if len(self.arguments) < min_args or len(self.arguments) > max_args:
            if max_args == min_args:
                msg = "%d" % min_args
            else:
                msg = "between %d and %d" % (min_args, max_args)
            raise SieveRuleSyntaxError("%s takes %s arguments" % (
                self.RULE_IDENTIFIER, msg))

    def validate_tests_size(self, min_tests, max_tests=None):
        if max_tests is None:
            max_tests = min_tests
        if len(self.tests) < min_tests or len(self.tests) > max_tests:
            if max_tests == min_tests:
                msg = "%d" % min_tests
            else:
                msg = "between %d and %d" % (min_tests, max_tests)
            raise SieveRuleSyntaxError("%s takes %s tests" % (
                self.RULE_IDENTIFIER, msg))

    def validate_arg_is_stringlist(self, index, length=None):
        if not (isinstance(self.arguments[index], list)
                and all(isinstance(arg, basestring)
                        for arg in self.arguments[index])):
            raise SieveRuleSyntaxError(
                    "%s requires argument %d to be a string or list of strings"
                    % (self.RULE_IDENTIFIER, index)
                    )
        if length is not None and len(self.arguments[index]) != length:
            if length == 1:
                msg = "a single string or list of one string"
            else:
                msg = "a list of %d strings" % length
            raise SieveRuleSyntaxError("%s requires argument %d to be %s" % (
                self.RULE_IDENTIFIER, index, msg))

    def validate_arg_is_tag(self, index, allowed_tags=None):
        if not isinstance(self.arguments[index], base.SieveTag):
            raise SieveRuleSyntaxError("%s requires argument %d to be a tag" %
                    (self.RULE_IDENTIFIER, index))
        if (allowed_tags is not None
                and self.arguments[index].tag not in allowed_tags):
            raise SieveRuleSyntaxError(
                    "%s requires argument %d to be one of these tags: %s"
                    % (self.RULE_IDENTIFIER, index,
                        ", ".join([ ":"+tag for tag in allowed_tags]))
                    )

    def validate_arg_is_number(self, index):
        try:
            long(self.arguments[index])
        except TypeError:
            raise SieveRuleSyntaxError("%s requires argument %d to be a number"
                    % (self.RULE_IDENTIFIER, index))

    def evaluate(self, message, state):
        raise NotImplementedError


class SieveCommand(SieveRule):

    def __init__(self, arguments=None, tests=None, block=None):
        SieveRule.__init__(self, arguments, tests)
        if block is None:
            self.block = SieveCommandList()
        else:
            self.block = block

    def __str__(self):
        s = SieveRule.__str__(self)
        if len(self.block.commands) > 0:
            s += "{\n"
            for command in self.block.commands:
                s += indent_string(str(command), 2)
            s += "}\n"
        return s

    def validate_block_size(self, max_commands):
        if len(self.block.commands) > max_commands:
            raise SieveRuleSyntaxError("%s takes no more than %d commands" % (
                self.RULE_IDENTIFIER, max_commands))


class SieveTest(SieveRule):

    def __init__(self, arguments=None, tests=None):
        SieveRule.__init__(self, arguments, tests)


class SieveCommandList(object):

    def __init__(self, command_list=None):
        if command_list is None:
            self.commands = []
        else:
            self.commands = command_list

    def __str__(self):
        return "".join(cmd.__str__() for cmd in self.commands)

    def evaluate(self, message, state=None):
        if state is None:
            state = { 'actions' : [], }
        return filter(lambda x: x is not None,
                (cmd.evaluate(message, state) for cmd in self.commands))


class SieveTag(object):

    TAG_CACHE = {}

    def __new__(cls, tag):
        instance = SieveTag.TAG_CACHE.get(tag)
        if instance is None:
            instance = object.__new__(cls)
            instance.tag = tag
            SieveTag.TAG_CACHE[tag] = instance
        return instance

    def __str__(self):
        return ":%s" % self.tag

    def __repr__(self):
        return "%s('%s')" % (self.__class__.__name__, self.tag)

class SieveTestHeader(SieveTest):
    RULE_IDENTIFIER = "HEADER"
register_sieve_test(SieveTestHeader)
class SieveTestAddress(SieveTest):
    RULE_IDENTIFIER = "ADDRESS"
register_sieve_test(SieveTestAddress)
class SieveCommandKeep(SieveCommand):
    RULE_IDENTIFIER = "KEEP"
register_sieve_command(SieveCommandKeep)
class SieveCommandFileinto(SieveCommand):
    RULE_IDENTIFIER = "FILEINTO"
register_sieve_command(SieveCommandFileinto)

