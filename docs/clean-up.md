# Perfrom Clean-Ups

It might happen that a prompt is cancelled by the user and clean-up actions
need to be performed. This can be achieved by using a `try-except`-block.

```python
from pathlib import Path
from aprompt import prompt
from aprompt.prompts import text

CACHE = Path("cache")

username = prompt("Please enter your username.", text())
CACHE.write_text(f"username={username}")

try:
    password = prompt("Please enter your password.", text(hide=True))
except SystemExit as exc:
    CACHE.write_text("")  # erease the cache
    raise exc

CACHE.write_text(CACHE.read_text() + f"\npassword={password}")
```

Prompts can be configured to be exited with {kbd}`CTRL+D`. The differnce to
exiting normally with {kbd}`CTRL+C` is that the program should not exit but
instead move on to the next or previous prompt. This option is usually used to
implement an undo operation.

```python
from pathlib import Path
from aprompt import prompt
from aprompt.exceptions import PromptExit
from aprompt.prompts import text

CACHE = Path("cache")

# ... WIP ...
```
