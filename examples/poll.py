from aprompt import prompt
from aprompt.prompts import choice, sort

prompt(
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

prompt(
    "Sort these langauge by their simplicity.",
    sort(
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
    )
)
