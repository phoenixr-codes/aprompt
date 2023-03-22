# Custom Widgets

Widgets can be seen as containers such as tags in XML/HTML. They are
yielded by prompt engines with several data required to be formatted
by a [formatter](#aprompt.formatters).

The [widgets module](#aprompt.widgets) module contains a collection
of widgets used by the built-in prompt engines as well as the base
class for widgets. In order to create a widget, we need to subclass
that base class:

```{attention}
[attrs](https://www.attrs.org/en/stable/) is used for the creation of
widgets in *aprompt*. To avoid third-party dependencies, we use
{external+python:py:func}`dataclasses.dataclass`es.
throughout the tutorial.
```

```{code-block} python
---
caption: src/aprompt_year/widgets.py
name: widgets-py
---
from dataclasses import dataclass
from aprompt.widgets import Widget

@dataclass
class Year(Widgets):
    value: int
```
