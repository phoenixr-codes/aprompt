"""
The *argparse* extension can be used to prompt the user arguments that
have not been set in the command-line. This has a similar effect as the
``prompt`` parameter in :external+click:py:class:`click.Option`.

Example:

.. code-block:: python

    from argparse import ArgumentParser
    from aprompt.ext.argparse import Namespace, PromptIfAbsent
    from aprompt.prompts import number

    parser = ArgumentParser(description="Example of argparse extension.")

    parser.add_argument(
        "--age",
        default=PromptIfAbsent(
            "Please enter your age.",
            number(minimum=0, maximum=150)
        )
    )

    args = parser.parse_args(namespace=Namespace()).prompt()
    print(args)
"""

from __future__ import annotations

import argparse
from functools import partial
from typing import Any

from aprompt import prompt


# TODO: documentation of __init__ and the class object
class PromptIfAbsent(partial):
    """
    A class to prompt for a value if it has not been provided in the
    command-line. This class is a subclass of
    :external+python:py:func:`functools.partial`
    with the difference that the function (:func:`aprompt.prompt`) does
    not need to be provided.
    """

    def __new__(cls, *args: Any, **kwargs: Any) -> PromptIfAbsent:
        return super().__new__(cls, prompt, *args, **kwargs)


class Namespace(argparse.Namespace):
    """
    A subclass of
    :external+python:py:class:`argparse.Namespace`
    that prompts for arguments with a default value of an instance of
    :class:`PromptIfAbsent` if they have not been provided in the
    command-line.

    To invoke the prompts, call :meth:`prompt` on the object returned by
    :external+python:py:meth:`argparse.ArgumentParser.parse_args`.
    """

    def __setattr__(self, name: str, value: Any) -> None:
        return super().__setattr__(name, value)

    def prompt(self) -> Namespace:
        for name, value in self.__dict__.items():
            if isinstance(value, PromptIfAbsent):
                setattr(self, name, value())
        return self
