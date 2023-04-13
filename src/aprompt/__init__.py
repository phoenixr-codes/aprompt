from __future__ import annotations

from collections.abc import Callable, Generator, Iterator
from functools import partial
import os
import signal
import sys
from typing import Any, Optional, TextIO, TypeVar

import readchar
from readchar import key as k, readkey

from aprompt import exceptions
from aprompt import formatters
from aprompt import widgets as w
from aprompt.result import Result
from aprompt._utils import clear_lines

T = TypeVar("T")

Key = str
PromptEngine = Generator[list[Optional[w.Widget]] | Result[T], Key, None]

readchar.config.INTERRUPT_KEYS = []  # manually handle `CTRL` + `C`


def prompt(
    ask: str,
    prompt_fn: PromptEngine[T],
    *,
    validate: None | Callable[[T], bool] | Callable[[T], BaseException | None] = None,
    formatter: Optional[formatters.Formatter] = None,
    file: Optional[TextIO] = None,
    cancelable: bool = False,
    test_with: Optional[Iterator[str]] = None,
) -> T:
    """
    Displays and formats the prompt, reads keys and handles validation.

    .. note::

        The prompt engine will be closed before an exception is raised or
        a value is returned.

    Example
    -------
    .. code-block:: python

        from aprompt import prompt
        from aprompt.prompts import confirm

        username = prompt(
            "Please enter a username.",
            text(placeholder="funkydog12"),
            validate=lambda name: bool(name)
        )

    Parameters
    ----------
    ask
        The question to ask / The prompt text.

    prompt_fn
        The prompt engine.

    validate
        A callable returning ``True``/``False`` or an instance of
        ``BaseException``/``None`` depending on the result.

        If the validation fails, the prompt will continue.

    formatter
        Defaults to :func:`aprompt.formatters.simple`.

    file
        The file to write to. Defaults to standard output.

    cancelable
        If this is set to ``True``,
        :class:`aprompt.exceptions.PromptExit` is raised when
        the user hits :kbd:`CTRL+D`. Only use this if you need
        to perform clean-up code for a single prompt. The program
        should not terminate so catching the exception with
        a ``try-except``-block is required.

        If this is set to ``False`` (default) nothing happens and
        :kbd:`CTRL+D` is sent to the prompt engine as a key.

        .. seealso::

            The :doc:`Perfrom Clean-Ups <../clean-up>` section
            describes how to handle :kbd:`CTRL+C` and :kbd:`CTRL+D.`.

    test_with
        Optional iterator of strings simulating keys to be
        pressed.

        .. seealso::

            The ``tests`` directory in the repository contains tests
            using this parameter:
            https://github.com/phoenixr-codes/aprompt/tree/main/tests

        .. seealso::

            The :doc:`Test API <../testing>` section describes how to
            use this parameter for tests in detail.

    Raises
    ------
    ``SystemExit``
        User hit :kbd:`CTRL+C`.

    :class:`aprompt.exceptions.PromptExit`
        User hit :kbd:`CTRL+D`. This is only raised when
        ``cancelable`` is set to ``True``.

    :class:`aprompt.exceptions.PromptNeverFinishedError`
        The prompt has never finished.

    :class:`aprompt.exceptions.PromptFinishedTooEarlyError`
        Not all keys from ``test_with`` were consumed from.

    Returns
    -------
    The (unwrapped) result of ``prompt_fn``.
    """
    validate = validate or (lambda _: True)
    file = file or sys.stdout

    fmt = partial(
        formatter or formatters.simple,
        os.get_terminal_size(file.fileno())
        if file.isatty() and test_with is None
        else os.terminal_size(
            (80, 24)
        ),  # prevent unnecessary possible `OSError`s when testing
    )

    def write(*args: Any, **kwargs: Any) -> None:
        if test_with is None:
            print(*args, **kwargs, file=file, end="")

    res = next(prompt_fn)
    assert not isinstance(res, Result)  # prompts must not initially yield a Result
    widgets: list[Optional[w.Widget]] = [w.Question(ask), *res]

    clear = 0
    while True:
        write(clear_lines(clear))
        display = "\n".join(fmt(widgets))
        write(display)
        clear = display.count("\n")

        if test_with is None:
            key = readkey()
        else:
            try:
                key = next(test_with)
            except StopIteration as exc:
                prompt_fn.close()
                raise exceptions.PromptNeverFinishedError(
                    f"prompt has never finished / ran out of keys"
                ) from exc

        if key == k.CTRL_C:
            prompt_fn.close()
            sys.exit(signal.Signals.SIGINT)
        elif key == k.CTRL_D and cancelable:
            prompt_fn.close()
            raise exceptions.PromptExit

        res = prompt_fn.send(key)
        if isinstance(res, Result):
            result = res.value
            match validate(result):
                case True | None:
                    write(clear_lines(clear))
                    write("\n".join(fmt([w.Question(ask), w.Answer(res.display)])))
                    write("\n")
                    prompt_fn.close()
                    if test_with is not None:
                        left = list(test_with)
                        if left:
                            raise exceptions.PromptFinishedTooEarlyError(
                                f"prompt has never finished; left keys: {left}",
                                left_keys=left,
                            )
                    return result
                # TODO: `case isinstance(e, BaseException)` might work as well
                case e:
                    if isinstance(e, BaseException):
                        widgets.append(w.Error(e))
                    else:
                        widgets.append(w.Alert())
                    next(
                        prompt_fn
                    )  # resume prompt because `yield Result` must not receive a key
        else:
            widgets = [w.Question(ask), *res]
