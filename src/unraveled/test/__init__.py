import pathlib

SOURCE_ROOT = pathlib.Path(__file__).parent.parent
_REPO_ROOT = SOURCE_ROOT.parent.parent

__all__ = [
    "SOURCE_ROOT",
    "_REPO_ROOT",
]
