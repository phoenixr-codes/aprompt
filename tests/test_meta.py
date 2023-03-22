"""
The tests in this file test if the aprompt test API works. If these tests
fail the test results of the other tests are likely going to be incorrect.
"""

from aprompt import prompt
from aprompt.exceptions import PromptFinishedTooEarlyError, PromptNeverFinishedError
from aprompt.prompts import confirm

import pytest

@pytest.mark.meta
def test_early_finished() -> None:
    with pytest.raises(PromptFinishedTooEarlyError) as exc_info:
        prompt(
            "",
            confirm(),
            test_with=iter("yabc")  # nothing is expected after 'y' or 'n'
        )
    assert exc_info.value.left_keys == list("abc")

@pytest.mark.meta
def test_never_finished() -> None:
    with pytest.raises(PromptNeverFinishedError):
        prompt(
            "",
            confirm(),
            test_with=iter("")  # atleast 'y' or 'n' is expected
        )