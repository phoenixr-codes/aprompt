aprompt - Advanced Prompt
=========================

Why use `input()` when you can go _advanced_?

*aprompt* lets you prompt users in a neat way. It comes with a UI system
and everything is customizable!

![Demonstration](https://raw.githubusercontent.com/phoenixr-codes/aprompt/main/docs/media/prompt-choice.gif)

[![Documentation Status](https://readthedocs.org/projects/aprompt/badge/?version=latest)](https://aprompt.readthedocs.io/en/latest/?badge=latest)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Features
--------

* ✅ Large set of built-in prompts.
* ✅ Custom prompts
* ✅ Custom themes
* ✅ Drop-in replacement for
  [argparse](https://docs.python.org/3/library/argparse.html?highlight=argparse#module-argparse)
* ✅ Test API


Available Prompts
-----------------

While it is easily possible to create custom prompts, aprompt comes with
a lot of useful prompts.

* [x] Text
* [x] Integer
* [x] Confirmation
* [x] PIN Code
* [x] Sort
* [x] Choice
* [x] Multiple Choice
* [ ] Path
* [ ] Datetime
* [ ] Date
* [ ] Time

_Unchecked prompts are planned for the future_


Basic Usage
-----------

```python
from aprompt import prompt
from aprompt.prompts import choice

languages: list[str] = prompt(
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

# ... do something with `languages` ...
```

Test API
--------

*aprompt* provides the attribute `test_with` for the main prompt wrapper to
test the result for a predefined sequence of keys.

```python
def test_n() -> None:
    assert not prompt("", confirm(), test_with=iter("n\n"))
```


Links
-----

* [🐍 Repo](https://github.com/phoenixr-codes/aprompt)
* [📦 PyPI](https://pypi.org/project/aprompt)
* [📖 Docs](https://aprompt.readthedocs.io/)


ToDo
----

* add path prompt (as extension) and document it
* turn `match`es to `if-else`s
* add demo file and add a GIF of it to the README (instead of only the choice variant)
* add GIFs to all prompt engines docs
* turn simple formatter into a class
* add logo

