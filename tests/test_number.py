from aprompt import prompt
from aprompt.prompts import number

import pytest

def test_span() -> None:
    assert prompt("", number(minimum=0, maximum=1), test_with=iter("+\n")) == 1
    assert prompt("", number(minimum=0, maximum=1), test_with=iter("+++\n")) == 1

def test_invalid_span() -> None:
    with pytest.raises(ValueError):
        prompt("", number(minimum=10, maximum=5), test_with=iter(""))

def test_invalid_default() -> None:
    with pytest.raises(ValueError):
        prompt("", number(minimum=0, maximum=10, default=20), test_with=iter(""))
    
    with pytest.raises(ValueError):
        prompt("", number(minimum=10, maximum=20, default=5), test_with=iter(""))

def test_no_span() -> None:
    assert prompt("", number(default=-50), test_with=iter("++\n")) == -48
