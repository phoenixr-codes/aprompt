from aprompt import prompt
from aprompt.prompts import confirm

def test_y() -> None:
    assert prompt("", confirm(), test_with=iter("y"))

def test_n() -> None:
    assert not prompt("", confirm(), test_with=iter("n"))

def test_default() -> None:
    assert prompt("", confirm(), test_with=iter("\n"))
    assert not prompt("", confirm(default=False), test_with=iter("\n"))
