from datetime import date
from pathlib import Path
import subprocess

from aprompt import prompt, PromptEngine
from aprompt.prompts import choice, text, number

licenses = {
    f.stem: f.read_text()
    for f in Path(__file__).with_name("licenses").iterdir()
    if f.suffix == ".txt"
}

name = prompt(
    "Choose a license.",
    choice(
        *licenses.keys(),
        multiple=False
    )
)

substitution: dict[str, str] = {}
while True:
    try:
        result = licenses[name].format(**substitution)
    except KeyError as e:
        arg = e.args[0]
        p: PromptEngine
        if arg == "year":
            p = number(minimum=1970, maximum=3000, default=date.today().year)
        elif arg == "author":
            try:
                res = subprocess.run(
                    ["git", "config", "user.name"],
                    stdout=subprocess.PIPE
                )
            except Exception:
                username = "Author"
            else:
                username = res.stdout.strip().decode()
            p = text(hide=False, default=username, placeholder=username)
        else:
            p = text(hide=False)
        answer = str(prompt(
            f"Please enter the {arg}",
            p  # type: ignore
        ))
        substitution[arg] = answer
    else:
        break

print(result)
