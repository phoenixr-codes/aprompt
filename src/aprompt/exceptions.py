from __future__ import annotations

from typing import Optional
from attrs import define


class PromptExit(BaseException):
    """
    An exception raised when a prompt has been exited.

    .. seealso:: :func:`aprompt.prompt`
    """


@define
class PromptFinishedTooEarlyError(Exception):
    """
    An exception raised when not all pre-defined keys were consumed in a
    prompt.

    .. seealso:: :func:`aprompt.prompt`
    """

    message: Optional[str] = None
    left_keys: Optional[list[str]] = None
    """A list of keys that were not consumed."""


@define
class PromptNeverFinishedError(Exception):
    """
    An exception raised when there were more keys expected to finish the
    prompt.

    .. seealso:: :func:`aprompt.prompt`
    """

    message: Optional[str] = None
