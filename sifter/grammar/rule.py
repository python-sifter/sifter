from email.message import Message
from typing import (
    Any,
    Dict,
    Text,
    Optional,
    List,
    Tuple
)

from sifter.grammar.tag import Tag
from sifter.grammar.state import EvaluationState
from sifter.grammar.validator import Validator
import sifter.grammar
import sifter.handler
import sifter.utils

__all__ = ('Rule', 'RuleSyntaxError',)


class RuleSyntaxError(Exception):
    pass


class Rule(object):

    RULE_TYPE: Optional[Text] = None
    RULE_IDENTIFIER: Optional[Text] = None

    @classmethod
    def register(cls) -> None:
        try:
            sifter.handler.register(cls.RULE_TYPE, cls.RULE_IDENTIFIER, cls)
        except AttributeError:
            # this method shouldn't be called on the Rule class directly,
            # only on subclasses that implement specific rules
            raise NotImplementedError

    def __init__(self, arguments: Optional[List[Any]] = None, tests: Optional[List[Any]] = None) -> None:
        if arguments is None:
            self.arguments = []
        else:
            self.arguments = arguments
        if tests is None:
            self.tests = []
        else:
            self.tests = tests

    def __str__(self) -> Text:
        s = ["%s" % self.RULE_IDENTIFIER, ]
        for arg in self.arguments:
            s.append(" %s" % arg)
        s.append('\n')
        for test in self.tests:
            s.append("(\n%s)\n" % sifter.utils.indent_string(str(test), 2))
        return ''.join(s)

    def validate_arguments(
        self,
        tagged_args: Optional[Dict[Any, Any]] = None,
        positional_args: Optional[List[Validator]] = None
    ) -> Tuple[Dict[Any, Any], List[Any]]:
        if tagged_args is None:
            tagged_args = {}
        if positional_args is None:
            positional_args = []

        seen_args = {}
        i, n = 0, len(self.arguments)
        while i < n:
            if not isinstance(self.arguments[i], Tag):
                break
            num_valid_args = 0
            for arg_name, arg_validator in tagged_args.items():
                num_valid_args = arg_validator.validate(self.arguments, i)
                if num_valid_args is not None and num_valid_args > 0:
                    if arg_name in seen_args:
                        raise RuleSyntaxError(
                            "%s argument to %s was already seen earlier: %s" % (arg_name, self.RULE_IDENTIFIER, self.arguments[i])
                        )
                    seen_args[arg_name] = self.arguments[i:i + num_valid_args]
                    i += num_valid_args
                    break
            else:
                raise RuleSyntaxError(
                    "Unexpected tag argument '%s' to %s encountered" % (self.arguments[i], self.RULE_IDENTIFIER)
                )
        # TODO: make sure all non-optional tagged arguments were seen

        if len(positional_args) != (n - i):
            raise RuleSyntaxError(
                "%s requires %d positional arguments but %d were supplied"
                % (self.RULE_IDENTIFIER, len(positional_args), n - i)
            )

        for arg_position, arg_validator in enumerate(positional_args):
            if arg_validator.validate(self.arguments, i + arg_position) == 0:
                raise RuleSyntaxError(
                    "positional argument #%d to %s was not in the expected format"
                    % (arg_position + 1, self.RULE_IDENTIFIER)
                )

        return (seen_args, self.arguments[i:])

    def validate_tests_size(self, min_tests: int, max_tests: Optional[int] = None) -> None:
        if max_tests is None:
            max_tests = min_tests
        if len(self.tests) < min_tests or len(self.tests) > max_tests:
            if max_tests == min_tests:
                msg = "%d" % min_tests
            else:
                msg = "between %d and %d" % (min_tests, max_tests)
            raise RuleSyntaxError("%s takes %s tests" % (
                self.RULE_IDENTIFIER, msg))

    def evaluate(self, message: Message, state: EvaluationState) -> Optional[bool]:
        raise NotImplementedError
