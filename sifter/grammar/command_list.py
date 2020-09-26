from sifter.grammar.state import EvaluationState

__all__ = ('CommandList',)


class CommandList(object):

    def __init__(self, command_list=None):
        if command_list is None:
            self.commands = []
        else:
            self.commands = command_list

    def __str__(self):
        return ''.join(cmd.__str__() for cmd in self.commands)

    def evaluate(self, message, state=None):
        if state is None:
            state = EvaluationState()
        for command in self.commands:
            command.evaluate(message, state)
            # don't bother processing more commands if we hit a STOP. this
            # isn't required by the standard, but we might as well.
            if len(state.actions) > 0 and state.actions[-1][0] == 'stop':
                break
        if state.actions.implicit_keep:
            state.actions.append('keep')
        return state.actions
