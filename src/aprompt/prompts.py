"""
A collection of prompts to use within the main :func:`aprompt.prompt`
function.

While the prompts are documented to return something they internally
*yield* the final result. The documented result is actually returned by
:func:`aprompt.prompt`.
"""

from __future__ import annotations

from collections.abc import Callable, Container
from itertools import cycle, repeat
from typing import Any, Literal, Optional, overload

from readchar import key as k

from aprompt import PromptEngine, widgets as w
from aprompt.result import Result
from aprompt._utils import Cursor, swap


def confirm(*, default: bool = True) -> PromptEngine[bool]:
    """Prompts for a boolean value.

    .. image:: media/prompt-confirm.gif

    Parameters
    ----------
    default
        The default is used when neither yes or no are typed.
    """

    def as_str(value: bool) -> str:
        if value:
            return "yes"
        return "no"

    alert = False
    while True:
        key = yield [w.Alert() if alert else None, w.Confirm(default=default)]
        alert = False

        match key:
            case "y" | "Y":
                yield Result(True, display=as_str(True))
            case "n" | "N":
                yield Result(False, display=as_str(False))
            case k.ENTER:
                yield Result(default, display=as_str(default))
            case _:
                alert = True


def text(
    *,
    hide: bool = False,
    default: str = "",
    placeholder: Optional[str] = None,
    validate: Optional[Callable[[str], bool]] = None,
    double_enter: bool = False,
) -> PromptEngine[str]:
    """Prompts a text input.

    Parameters
    ----------
    hide
        Hides the entered text from the terminal.

    default
        A string that is returned when no text has been entered.

    placeholder
        A string giving the user an idea of what is expected.

    validate
        A callable taking the entered character as input and returning a
        boolean deciding whether to add it to the result. By default any
        character is accepted.

    double_enter
        Requires hitting the enter key twice to indicate that the text is
        done. This is useful for texts that contains newlines.
    """
    # TODO: key to hide/show text (only when hide is initially set to true)

    validate = validate or (lambda _: True)
    result = ""
    enter = False
    initial_hide = hide

    alert = False
    while True:
        key = yield [
            w.Alert() if alert else None,
            w.Text(result, placeholder=placeholder, hide=hide),
            w.Navigation({"CTRL + H": f"{'show' if hide else 'hide'} text"})
            if initial_hide
            else None,
        ]
        alert = False

        match key:
            case k.ENTER:
                if double_enter:
                    if enter:
                        yield Result(
                            result or default,
                            display="*" * len(result) if initial_hide else result,
                        )
                    else:
                        enter = True
                else:
                    yield Result(
                        result or default,
                        display="*" * len(result) if initial_hide else result,
                    )
            case k.BACKSPACE:
                if result:
                    result = result[:-1]
                    enter = False
                else:
                    alert = True
            case k.CTRL_H:
                if initial_hide:
                    hide = not hide
                else:
                    alert = True
            case k.UP | k.DOWN | k.PAGE_DOWN | k.PAGE_UP:
                # TODO: add cursor support
                alert = True
            case _:
                if validate(key):
                    result += key
                    enter = False
                else:
                    alert = True


def number(
    *,
    minimum: Optional[int] = None,
    maximum: Optional[int] = None,
    default: Optional[int] = None,
) -> PromptEngine[int]:
    """Prompts for an integer.

    Parameters
    ----------
    minimum
        Optional minimum value. This must be less than or equal to
        ``default``.

    maximum
        Optional maximum value. This must be less than or equal to
        ``default``.

    default
        The number to begin from. Defaults to ``minimum`` if specified,
        otherwise ``0`` or ``maximum`` if ``maximmum`` is greater than or
        equal to ``0``.
    """
    if default is None:
        if minimum is not None and maximum is not None and minimum > maximum:
            raise ValueError(
                f"minimum ({minimum}) cannot be greater than maximum ({maximum})"
            )
        default = (
            minimum
            if minimum is not None
            else maximum
            if maximum is not None and maximum <= 0
            else 0
        )
    else:
        if minimum is not None and default < minimum:
            raise ValueError(
                f"default ({default}) cannot be less than minimum ({minimum})"
            )
        if maximum is not None and default > maximum:
            raise ValueError(
                f"default ({default}) cannot be greater than maximum ({maximum})"
            )

    result = default

    alert = False
    while True:
        key = yield [
            w.Alert() if alert else None,
            w.Integer(result),
            w.Navigation(
                {
                    "ENTER": "done",
                    "+ OR \N{UPWARDS ARROW}": "increase",
                    "- OR \N{DOWNWARDS ARROW}": "decrease",
                }
            ),
        ]
        alert = False

        match key:
            case k.ENTER:
                yield Result(result)
            case k.UP | "+":
                result += 1
                if maximum is not None and result > maximum:
                    result -= 1
                    alert = True
            case k.DOWN | "-":
                result -= 1
                if minimum is not None and result < minimum:
                    result += 1
                    alert = True
            case _:
                alert = True


@overload
def choice(
    *choices: str,
    multiple: Literal[True],
    require: Callable[[int], bool] | int | Container[int] | None = None,
) -> PromptEngine[list[str]]:
    ...


@overload
def choice(
    *choices: str, multiple: Literal[False] = False, require: None = None
) -> PromptEngine[str]:
    ...


def choice(
    *choices: str,
    multiple: bool = False,
    require: Callable[[int], bool] | int | Container[int] | None = None,
) -> PromptEngine[list[str]] | PromptEngine[str]:
    """Prompts for options.

    .. image:: media/prompt-choice.gif
    
    .. versionadded:: 3.0.1
        ``require`` now accepts containers.

    Parameters
    ----------
    choices
        Options to choose from.

    multiple
        Makes selecting multiple options possible.

    require
        .. note::

            This parameter only has an effect when ``multiple``
            is set to ``True``.

        ``(int) → bool``
            A callable taking the amount of selected prompts as an
            integer as a single argument and returning a boolean
            whether to pass or deny the resut.

        ``Container[int]``
            A container (usually a ``range``) specifying possible amounts
            that are required to be selected.

        ``int``
            An integer specifying the amount of options that are
            required to be selected.

        This parameter can be used as a shorthand for the
        ``validate`` parameter of the :func:`aprompt.prompt`
        function:

        .. code-block:: python

            prompt("¿Que?", choice(..., multiple=True), validate=lambda choices: len(choices) == 5)

            # same as:

            prompt("¿Que?", choice(..., multiple=True, require=5))

    Returns
    -------
    A list of the options chosen if ``multiple`` is ``True``.
    The selected option if ``multiple`` is ``False``.
    """
    options: list[w.Option] = [
        w.Option(o, hover=not bool(i)) for i, o in enumerate(choices)
    ]

    if require is None:
        require = lambda _: True
    elif isinstance(require, int):
        require = lambda n: n == require
    elif not callable(require):
        # Container
        require = lambda n: n in require  # type: ignore

    alert = False
    while True:
        key = yield [w.Alert() if alert else None, w.Options(options)]
        alert = False

        match key:
            case k.ENTER:
                if multiple:
                    result = [o.content for o in options if o.select]
                    if require(len(result)):
                        yield Result(result, display=", ".join(result))
                    else:
                        alert = True
                else:
                    for o in options:
                        if o.hover:
                            yield Result(o.content)
                            break
                    else:
                        raise RuntimeError  # unreachable
            case k.DOWN:
                c = cycle(options)
                for i in c:
                    if i.hover:
                        i.hover = False
                        break
                next(c).hover = True
            case k.UP:
                c = cycle(reversed(options))
                for i in c:
                    if i.hover:
                        i.hover = False
                        break
                next(c).hover = True
            case k.SPACE:
                if multiple:
                    for o in options:
                        if o.hover:
                            o.select = not o.select
                else:
                    alert = True
            case _:
                alert = True


def sort(*choices: str) -> PromptEngine[list[str]]:
    options: list[w.Option] = [
        w.Option(o, hover=not bool(i)) for i, o in enumerate(choices)
    ]

    alert = False
    while True:
        key = yield [w.Alert() if alert else None, w.SortableOptions(options)]
        alert = False

        match key:
            case k.ENTER:
                result = [o.content for o in options]
                yield Result(result, display=", ".join(result))
            case k.SPACE:
                for o in options:
                    if o.hover:
                        o.select = not o.select
            case k.UP:
                cur = Cursor(options, [i for i, o in enumerate(options) if o.hover][0])
                hovered, i = cur.item, cur.index
                cur.prev()
                other, j = cur.item, cur.index
                if hovered.select:
                    swap(options, i, j)
                else:
                    hovered.hover = False
                    other.hover = True
            case k.DOWN:
                cur = Cursor(options, [i for i, o in enumerate(options) if o.hover][0])
                hovered, i = cur.item, cur.index
                cur.next()
                other, j = cur.item, cur.index
                if hovered.select:
                    swap(options, i, j)
                else:
                    hovered.hover = False
                    other.hover = True
            case _:
                alert = True


def pin(length: int, *, require_enter: bool = False) -> PromptEngine[list[int]]:
    """
    Parameters
    ----------
    length
        The length of the PIN code.

    require_enter
        By default, the prompt finishes when the last digit is entered.
        Setting this parameter to ``True`` will enforce hitting ``ENTER``
        to finish the prompt.

    Returns
    -------
    Each digit of the entered PIN code.
    """
    result: list[int] = []

    if length < 1:
        raise ValueError(f"length must be 1 or greater; got {length}")

    alert = False
    while True:
        key = yield [
            w.Alert() if alert else None,
            w.Code([*result, *repeat(None, length - len(result))]),
        ]
        alert = False

        if key == k.BACKSPACE:
            if result:
                result.pop()
            else:
                alert = True
        elif key == k.ENTER and require_enter and len(result) == length:
            yield Result(result, display="".join(map(str, result)))
        else:
            try:
                num = int(key)
            except ValueError:
                alert = True
            else:
                result.append(num)
                if not require_enter and len(result) == length:
                    yield Result(result, display="".join(map(str, result)))
