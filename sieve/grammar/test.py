from sieve.grammar.rule import SieveRule


class SieveTest(SieveRule):

    RULE_TYPE = 'test'

    def __init__(self, arguments=None, tests=None):
        super(SieveTest, self).__init__(arguments, tests)

