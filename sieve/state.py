from sieve.rules.actions import SieveActions

class SieveEvaluationState(object):

    def __init__(self):
        self.actions = SieveActions(implicit_keep=True)
        self.required_extensions = {}
        # section 6.1: the built-in comparators have defined capability
        # strings, but they do not need to be explicitly REQUIRE'd before being
        # used.
        for ext in ('comparator-i;octet', 'comparator-i;ascii-casemap'):
            self.require_extension(ext)

    def require_extension(self, extension):
        self.required_extensions[extension] = True
