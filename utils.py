import pathlib
import sys


def make_path(relative_path: str) -> pathlib.Path:
    if getattr(sys, "frozen", False):
        base_dir = sys._MEIPASS + "/"
    else:
        base_dir = ""
    path = pathlib.Path(base_dir + relative_path)

    return path
