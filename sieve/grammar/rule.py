import sieve.grammar
import sieve.handler
import sieve.utils

__all__ = ('Rule', 'RuleSyntaxError',)


class RuleSyntaxError(Exception):
    pass


class Rule(object):

    @classmethod
    def register(cls):
        try:
            sieve.handler.register(cls.RULE_TYPE, cls.RULE_IDENTIFIER, cls)
        except AttributeError:
            # this method shouldn't be called on the SieveRule class directly,
            # only on subclasses that implement specific rules
            raise NotImplementedError

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
            s.append("(\n%s)\n" % sieve.utils.indent_string(str(test), 2))
        return ''.join(s)

    def validate_arguments_size(self, min_args, max_args=None):
        if max_args is None:
            max_args = min_args
        if len(self.arguments) < min_args or len(self.arguments) > max_args:
            if max_args == min_args:
                msg = "%d" % min_args
            else:
                msg = "between %d and %d" % (min_args, max_args)
            raise RuleSyntaxError("%s takes %s arguments" % (
                self.RULE_IDENTIFIER, msg))

    def validate_tests_size(self, min_tests, max_tests=None):
        if max_tests is None:
            max_tests = min_tests
        if len(self.tests) < min_tests or len(self.tests) > max_tests:
            if max_tests == min_tests:
                msg = "%d" % min_tests
            else:
                msg = "between %d and %d" % (min_tests, max_tests)
            raise RuleSyntaxError("%s takes %s tests" % (
                self.RULE_IDENTIFIER, msg))

    def validate_arg_is_stringlist(self, index, length=None):
        if not (isinstance(self.arguments[index], list)
                and all(isinstance(arg, basestring)
                        for arg in self.arguments[index])):
            raise RuleSyntaxError(
                    "%s requires argument %d to be a string or list of strings"
                    % (self.RULE_IDENTIFIER, index)
                    )
        if length is not None and len(self.arguments[index]) != length:
            if length == 1:
                msg = "a single string or list of one string"
            else:
                msg = "a list of %d strings" % length
            raise RuleSyntaxError("%s requires argument %d to be %s" % (
                self.RULE_IDENTIFIER, index, msg))

    def validate_arg_is_tag(self, index, allowed_tags=None):
        if not isinstance(self.arguments[index], sieve.grammar.Tag):
            raise RuleSyntaxError("%s requires argument %d to be a tag" %
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
            raise RuleSyntaxError("%s requires argument %d to be a number"
                    % (self.RULE_IDENTIFIER, index))

    def validate_arg_is_comparator(self, index):
        self.validate_arg_is_stringlist(index, 1)
        if not sieve.handler.get('comparator', self.arguments[index][0]):
            raise RuleSyntaxError(
                    "'%s' comparator is unknown/unsupported"
                    % self.arguments[index][0])

    def validate_arg_is_match_type(self, index):
        self.validate_arg_is_tag(index, ('IS', 'CONTAINS', 'MATCHES'))

    def validate_arg_is_address_part(self, index):
        self.validate_arg_is_tag(index, ('LOCALPART', 'DOMAIN', 'ALL'))

    def evaluate(self, message, state):
        raise NotImplementedError

