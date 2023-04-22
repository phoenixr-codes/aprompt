# Quickstart

This page will guide you through the installation process and the creation
of your first prompt.

## Installation

You can install aprompt with [pip](https://pip.pypa.io/en/stable/):

```console
pip install -U aprompt
```

## Basic Usage

Each prompt consists of three main parts:

* The main {func}`aprompt.prompt` function.
* Its first argument: the prompt text or question.
* Its second argument: the prompt engine.

```python
from aprompt import prompt
from aprompt.prompts import choice

can_code_in = prompt(
    "In what languages can you code in?",
    choice(
        "c",
        "c++",
        "erlang",
        "fortran",
        "haskell",
        "javascript",
        "nim",
        "python",
        "ruby",
        "rust",
        "typescript",
        multiple=True
    )
)
```

Running this script will prompt you to select from the options above.
You may select none, one or more. The selected options will be returned
and saved into the variable `can_code_in`.


## Prompt vs Prompt Engine vs Prompt Function

You will often find the terms "prompt" and "prompt engine" in the
documentation:

Prompt
> A prompt is what you see on the terminal when the "prompt
> function" is called. You can interact with the prompt by pressing
> keys.

Prompt Engine
> A prompt engine is a generator that handles the keys pressed by the user
> and reacts with so called widgets.

Prompt Function
> The prompt function is the wrapper around the "prompt engine". It
> connects it with a formatter and manages the display.
> ```{seealso}
> {func}`aprompt.prompt`
> ```
