"""
Internal utilities for aprompt.
"""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any, Generic, TypeVar
from attrs import define

T = TypeVar("T")


def clear_lines(amount: int) -> str:
    """
    Returns ansi escape sequence that clears the last n lines.
    """
    return "\x1b[1A\x1b[2K\r" * amount


def swap(x: list[Any], pos1: int, pos2: int, /) -> None:
    """
    Swaps two items in a list.
    """
    x[pos1], x[pos2] = x[pos2], x[pos1]


def boolean(string: str) -> bool:
    if string.lower() in ["true", "yes"]:
        return True
    if string.lower() in ["false", "no"]:
        return False
    raise ValueError(f"expected 'true', 'yes', 'false' or 'no', got f{string!r}")


@define
class Cursor(Generic[T]):
    _list: list[T]
    _index: int = 0

    def __attrs_post_init__(self) -> None:
        self._index %= len(self._list)

    def __iter__(self) -> Iterator[T]:
        return iter(self._list)

    @property
    def item(self) -> T:
        return self._list[self._index]

    @property
    def index(self) -> int:
        return self._index

    def next(self) -> None:
        self._index += 1
        self._index %= len(self._list)

    def prev(self) -> None:
        self._index -= 1
        self._index %= len(self._list)
