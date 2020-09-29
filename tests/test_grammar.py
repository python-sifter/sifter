# type: ignore

import pytest

import sifter.extension
from sifter.grammar.state import EvaluationState


def test_grammar():
    sifter.extension.register('ext1')
    sifter.extension.register('ext2')
    state = EvaluationState()

    state.require_extension('ext1')

    assert state.check_required_extension('ext1', 'ext1') is True

    with pytest.raises(RuntimeError):
        state.check_required_extension('ext2', 'ext2')
