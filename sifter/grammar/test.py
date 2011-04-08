import rule

__all__ = ('Test',)


class Test(rule.Rule):

    RULE_TYPE = 'test'

    def __init__(self, arguments=None, tests=None):
        super(Test, self).__init__(arguments, tests)

