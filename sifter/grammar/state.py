from typing import (
    Text,
    Dict,
    Optional
)
from sifter.grammar.actions import Actions

__all__ = ('EvaluationState',)


class EvaluationState(object):

    def __init__(self) -> None:
        self.actions = Actions(implicit_keep=True)
        self.required_extensions: Dict[Text, bool] = {}
        self.last_if: Optional[bool] = None
        # section 6.1: the built-in comparators have defined capability
        # strings, but they do not need to be explicitly REQUIRE'd before being
        # used.
        for ext in ('comparator-i;octet', 'comparator-i;ascii-casemap'):
            self.require_extension(ext)

    def require_extension(self, extension: Text) -> None:
        self.required_extensions[extension] = True

    def check_required_extension(self, extension: Text, feature_string: Text) -> bool:
        if extension not in self.required_extensions:
            raise RuntimeError(
                "REQUIRE '%s' must happen before %s can be used."
                % (extension, feature_string)
            )
        return True
