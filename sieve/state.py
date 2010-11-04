from sieve.rules.actions import SieveActions

class SieveEvaluationState(object):

    def __init__(self):
        self.actions = SieveActions(implicit_keep=True)
