import sys
from ast import AST
from typing import Any, Generator, Tuple, Type

if sys.version_info < (3, 8):
    import importlib_metadata
else:
    import importlib.metadata as importlib_metadata

from flake8_loopy.error_codes import ERROR_CODES
from flake8_loopy.visitor import Visitor


class LoopyPlugin:
    name = __name__
    version = importlib_metadata.version(__name__)

    def __init__(self, tree: AST) -> None:
        self._tree = tree

    def run(self) -> Generator[Tuple[int, int, str, Type[Any]], None, None]:
        visitor = Visitor()
        visitor.visit(self._tree)
        # Write errors for unused variables
        for line, col, code, unused in visitor.errors:
            msg = f"LPY{code} {ERROR_CODES[code].format(var=unused)}"
            yield line, col, msg, type(self)


__all__ = ["LoopyPlugin"]
