from pathlib import Path

from aprompt import PromptEngine
from aprompt.ext.path import widgets as w
from aprompt.widgets import Alert, Navigation


def path(
    root: Path | str,
    *,
    allow_creation: bool = False,
    require_file: bool = False,
    multiple_files: bool = False,
) -> PromptEngine[list[Path] | Path]:
    current = Path(root).resolve()
    selected: list[Path] = []

    if not require_file:
        multiple_files = False

    alert = False
    while True:
        key = yield [
            Alert() if alert else None,
            w.Path(current),
            w.SelectedPaths(selected) if multiple_files else None,
            Navigation(
                {
                    **(
                        {"\N{LEFTWARDS ARROW}": "goto parent directory"}
                        if current.root != str(current)
                        else {}
                    ),
                    **(
                        {"\N{RIGHTWARDS ARROW}": "enter directory"}
                        if current.is_dir()
                        else {}
                    ),
                    **({"[SPACE]": "select file"} if multiple_files else {}),
                    "[ENTER]": f"select path{'s' if len(selected) > 1 else ''}",
                }
            ),
        ]
