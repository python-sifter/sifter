import sieve.handler
from sieve.rules import actions
from sieve.state import SieveEvaluationState

def indent_string(s, num_spaces):
    add_newline = False
    if s[-1] == '\n':
        add_newline = True
        s = s[:-1]
    s = '\n'.join(num_spaces * ' ' + line for line in s.split('\n'))
    if add_newline: s += '\n'
    return s

def find_implementations(cls, impl_identifier_fn):
    impl_map = {}
    classes = [ cls, ]
    while len(classes) > 0:
        c = classes.pop()
        try:
            impl_id = impl_identifier_fn(c)
            impl_map[impl_id] = c
        except AttributeError:
            classes.extend(c.__subclasses__())
    return impl_map


class SieveRuleSyntaxError(Exception):
    pass


class SieveRule(object):

    @classmethod
    def register_imported_rules(cls):
        try:
            cls._RULE_MAP = find_implementations(cls,
                    lambda impl: impl.RULE_IDENTIFIER)
        except AttributeError:
            # this method shouldn't be called on the SieveRule class directly,
            # only on subclasses
            raise NotImplementedError

    @classmethod
    def get_rule_handler(cls, rule_name):
        try:
            return cls._RULE_MAP.get(rule_name)
        except AttributeError:
            # this method shouldn't be called on the SieveRule class directly,
            # only on subclasses
            return NotImplementedError

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
        s = [ "%s" % self.RULE_IDENTIFIER, ]
        for arg in self.arguments:
            s.append(" %s" % arg)
        s.append('\n')
        for test in self.tests:
            s.append("(\n%s)\n" % indent_string(str(test), 2))
        return ''.join(s)

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
        if not isinstance(self.arguments[index], SieveTag):
            raise SieveRuleSyntaxError("%s requires argument %d to be a tag" %
                    (self.RULE_IDENTIFIER, index))
        if (allowed_tags is not None
                and self.arguments[index].tag not in allowed_tags):
            raise SieveRuleSyntaxError(
                    "%s requires argument %d to be one of these tags: %s"
                    % (self.RULE_IDENTIFIER, index,
                        ', '.join([ ':'+tag for tag in allowed_tags]))
                    )

    def validate_arg_is_number(self, index):
        try:
            long(self.arguments[index])
        except TypeError:
            raise SieveRuleSyntaxError("%s requires argument %d to be a number"
                    % (self.RULE_IDENTIFIER, index))

    def validate_arg_is_comparator(self, index):
        self.validate_arg_is_stringlist(index, 1)
        if not sieve.handler.get('comparator', self.arguments[index][0]):
            raise SieveRuleSyntaxError(
                    "'%s' comparator is unknown/unsupported"
                    % self.arguments[index][0])

    def validate_arg_is_match_type(self, index):
        self.validate_arg_is_tag(index, ('IS', 'CONTAINS', 'MATCHES'))

    def validate_arg_is_address_part(self, index):
        self.validate_arg_is_tag(index, ('LOCALPART', 'DOMAIN', 'ALL'))

    def evaluate(self, message, state):
        raise NotImplementedError


class SieveCommand(SieveRule):

    _RULE_MAP = {}

    def __init__(self, arguments=None, tests=None, block=None):
        SieveRule.__init__(self, arguments, tests)
        if block is None:
            self.block = SieveCommandList()
        else:
            self.block = block

    def __str__(self):
        s = [ SieveRule.__str__(self), ]
        if len(self.block.commands) > 0:
            s.append("{\n")
            for command in self.block.commands:
                s.append(indent_string(str(command), 2))
            s.append("}\n")
        return ''.join(s)

    def validate_block_size(self, max_commands):
        if len(self.block.commands) > max_commands:
            raise SieveRuleSyntaxError("%s takes no more than %d commands" % (
                self.RULE_IDENTIFIER, max_commands))


class SieveTest(SieveRule):

    _RULE_MAP = {}

    def __init__(self, arguments=None, tests=None):
        SieveRule.__init__(self, arguments, tests)


class SieveCommandList(object):

    def __init__(self, command_list=None):
        if command_list is None:
            self.commands = []
        else:
            self.commands = command_list

    def __str__(self):
        return ''.join(cmd.__str__() for cmd in self.commands)

    def evaluate(self, message, state=None):
        if state is None:
            state = SieveEvaluationState()
        for command in self.commands:
            command.evaluate(message, state)
            # don't bother processing more commands if we hit a STOP. this
            # isn't required by the standard, but we might as well.
            if len(state.actions) > 0 and state.actions[-1][0] == 'stop':
                break
        return state.actions


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

