from sieve.rules.actions import SieveActions

class SieveEvaluationState(object):

    def __init__(self):
        self.actions = SieveActions(implicit_keep=True)
        self.required_extensions = {}

    def require_extension(self, extension):
        self.required_extensions[extension] = True
