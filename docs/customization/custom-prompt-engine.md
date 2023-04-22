# Custom Prompt Engine

The heart of the extension is the actual prompt engine. It reacts on
pressed keys and manages widgets.


## Structure

Each prompt engine has the same base structure:

```{code-block} python
---
linenos: true
emphasize-lines: 6,7,8,9,16,17
---
from aprompt import PromptEngine
from aprompt.result import Result
from readchar import keys as k

def my_prompt(arguments) -> PromptEngine[ResultType]:
    alert = False
    while True:
        key = yield [
            w.Alert() if alert else None,
            widget1,
            widget2,
            ...
        ]
        alert = False

        if key == k.ENTER:
            yield Result(result, display="display")
        elif ...:
            ...
        else:
            alert = True
```

````{list-table}
---
header-rows: 1
---

* - Line
  - Purpose
* - 6
  - Alerts are used to signal the user that an invalid input has been
    entered.
* - 7
  - An infinite loop is required for prompt engines.
* - 8
  - [Yield expressions](https://docs.python.org/3/reference/expressions.html#yield-expressions)
    that receive a value are rarely used in python and may be complicated
    to understand. Just remember the following term:
    We *receive* a key pressed by the user after we *send* widgets.
* - 9
  - The [Alert widget](#aprompt.widgets.Alert) is a special widget that
    tells the formatter to notify the user an invalid input got sent.
    We only do that if `alert` is set to `True`. Otherwise we use
    `None`. `None` is allowed to be sent to allow
    [conditional expressions](https://peps.python.org/pep-0308/).
* - 16
  - Match the key for different values.
* - 17
  - When we are done we wrap the result inside a
    {class}`aprompt.result.Result`.
    
    ```{caution}
    The prompt engine may resume at this point when a validation fails.
    ```
````

* A prompt engine must not initially yield a
  {class}`aprompt.result.Result`.
* A prompt engine is closed by {func}`aprompt.prompt` before it
  raises or returns anything.


## Begin

```python
from aprompt import PromptEngine
from aprompt.widgets import Alert

def path() -> PromptEngine:
    alert = False
    while True:
      key = yield [
          Alert() if alert else None,
          # TODO
      ]
      alert = False
```

Our prompt engine should take the following arguments:

* `root`
  > The path to display at the beginning.
* `allow_creation`
  > Allows to create directories and files.
* `require_file`
  > Requires a file to be selected instead of a directory.
* `multiple_files`
  > Multiple files may be selected.

... WIP ...
