from sifter.grammar.rule import Rule

__all__ = ('Test',)


class Test(Rule):

    RULE_TYPE = 'test'

    def __init__(self, arguments=None, tests=None):
        super(Test, self).__init__(arguments, tests)
