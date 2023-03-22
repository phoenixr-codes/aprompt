import pathlib
from attrs import define
from aprompt.widgets import Widget


@define
class Path(Widget):
    path: pathlib.Path


@define
class SelectedPaths(Widget):
    paths: list[Path]
