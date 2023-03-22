from abc import ABC
from typing import Any, Optional
from attrs import define, field


class Widget(ABC):
    """
    A widget defines an item displayed on the terminal.
    """


@define
class Alert(Widget):
    """
    This widget does not display anything but rather indicates that the
    bell should be activated. This is commonly used when an invalid input
    is entered.
    """


@define
class Question(Widget):
    content: str


@define
class Answer(Widget):
    content: Any


@define
class Error(Widget):
    content: BaseException


@define
class Navigation(Widget):
    content: dict[str, str]


@define
class Text(Widget):
    content: str
    placeholder: Optional[str] = field(kw_only=True)
    hide: bool = field(kw_only=True)


@define
class Option(Widget):
    content: str
    select: Optional[bool] = field(kw_only=True, default=None)
    hover: Optional[bool] = field(kw_only=True, default=None)


@define
class Options(Widget):
    content: list[Option]


@define
class SortableOptions(Widget):
    content: list[Option]


@define
class Confirm(Widget):
    default: bool


@define
class Integer(Widget):
    content: int


@define
class Code(Widget):
    content: list[Optional[int]]
