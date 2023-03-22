from __future__ import annotations
from typing import Generic, TypeVar
from attr import define, field

T = TypeVar("T")


@define
class Result(Generic[T]):
    """
    A class indicating the result of a prompt function. This is used
    instead of a return value for the case that a post-validation
    fails.

    Parameters
    ----------
    value
        The result of the prompt.

    display
        A string displayed in the terminal represing the result.
        Defaults to ``str(value)``.
    """

    value: T
    display: str = field(kw_only=True)

    @display.default
    def _(self) -> str:
        return str(self.value)
