from aprompt import prompt
from aprompt.prompts import pin

import pytest

def test_normal()-> None:
    assert prompt("", pin(4), test_with=iter("1234")) == [1, 2, 3, 4]

def test_invalid_length() -> None:
    with pytest.raises(ValueError):
        prompt("", pin(0), test_with=iter(""))
    
    with pytest.raises(ValueError):
        prompt("", pin(-5), test_with=iter(""))

def test_nan() -> None:
    assert prompt("", pin(4), test_with=iter("12x34")) == [1, 2, 3 , 4]

def test_require_enter() -> None:
    assert prompt("", pin(4, require_enter=True), test_with=iter("1234\n")) == [1, 2, 3, 4]
    assert prompt("", pin(4, require_enter=True), test_with=iter("12\n34\n")) ==  [1, 2, 3, 4]
