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
    CACHE.write_text("")
    raise exc

CACHE.write_text(CACHE.read_text() + f"\npassword={password}")

```
