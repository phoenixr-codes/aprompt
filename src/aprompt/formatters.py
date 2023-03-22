r"""
Formatters take :class:`aprompt.widgets.Widget`\s as input and return a
string representing it by using the widget's data.
"""

from __future__ import annotations

from collections.abc import Callable
from functools import partial
import os
import textwrap
from typing import Optional

from aprompt import widgets as w

Formatter = Callable[[os.terminal_size, list[Optional[w.Widget]]], list[str]]


def simple(
    tsize: os.terminal_size,
    widgets: list[Optional[w.Widget]],
) -> list[str]:
    fill = partial(textwrap.fill, width=tsize.columns, replace_whitespace=False)

    header: list[str] = []
    body: list[str] = []
    footer: list[str] = []

    for widget in widgets:
        # sepcial widgets
        if isinstance(widget, w.Alert):
            header.insert(0, "\a")
        if isinstance(widget, w.Answer):
            header.append(fill(str(widget.content), initial_indent="> ") or "> (none)")

        # first-class widgets
        if isinstance(widget, w.Question):
            header.insert(0, fill(widget.content, initial_indent="? "))
        if isinstance(widget, w.Error):
            footer.append(fill(str(widget.content), initial_indent="! "))
        if isinstance(widget, w.Navigation):
            lines: list[str] = []
            for pair in widget.content.items():
                lines.append("  " + ": ".join(pair))
            footer.append("NAVIGATION\n" + "\n".join(lines))

        # other widgets
        if isinstance(widget, w.Text):
            if not widget.content and widget.placeholder is not None:
                body.append(fill(f"(e.g.: {widget.placeholder})"))
            else:
                body.append(
                    fill(("*" * len(widget.content)) if widget.hide else widget.content)
                )
        if isinstance(widget, w.Confirm):
            body.append(fill(f"y/n [{'y' if widget.default else 'n'}]"))
        if isinstance(widget, w.Integer):
            body.append(fill(f"+/- {widget.content}"))
        if isinstance(widget, w.Options):
            for o in widget.content:
                body.append(
                    fill(
                        o.content,
                        initial_indent=("x" if o.select else " ")
                        + (">" if o.hover else " ")
                        + " ",
                    )
                )
        if isinstance(widget, w.SortableOptions):
            for o in widget.content:
                body.append(
                    fill(
                        o.content,
                        initial_indent=("|" if o.select else ">" if o.hover else " ")
                        + " ",
                    )
                )
        if isinstance(widget, w.Code):
            body.append(
                " ".join(
                    map(lambda num: "_" if num is None else str(num), widget.content)
                )
            )

        # unknown widgets
        if isinstance(w, w.Widget):
            body.append(fill(str(widget)))

    return [*header, *body, *footer, ""]
