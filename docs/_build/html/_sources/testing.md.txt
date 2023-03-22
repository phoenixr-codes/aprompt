# Test API

*aprompt* provides a test API for prompts. Instead of typing the keys in
the command-line, they can be programmatically predefined. The
:func:`aprompt.prompt` function will raise appropriate errors when there
were too many or too few predefined keys.

The
[``tests`` directory in the repository](https://github.com/phoenixr-codes/aprompt/tree/main/tests) contains tests
using this parameter.

Lets write a test for the built-in {func}`aprompt.prompts.number` prompt:

```{code-block} python
---
emphasize-lines: 5
---
from aprompt import prompt
from aprompt.prompts import number

def test_increase():
    assert prompt("", number(default=10), test_with=iter("+++\n")) == 13

if __name__ == "__main__":
    test_increase()
```

The highlighted line is the only thing we need to concentrate about. We
create a prompt like usual with some minor differences:

* The first argument is an empty string.
  > We don't need any text for the question because nothing will be
  > displayed.
* `test_with` is defined.
  > In order to tell the prompt what keys we want to simulate, we set
  > the `test_with` argument to an iterator. The three plusses simulate
  > the normal {kbd}`+` key (three times). The newline at the end
  > represents the {kbd}`ENTER` key.

The prompt returns the same result as we would get by typing the keys
in the command-line - the integer 13.