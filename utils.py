from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, TypeVar, overload

if TYPE_CHECKING:
    from typing import Any, Callable, Literal

T = TypeVar("T")


@overload
def load(filename: str, reader: Literal["lines"]) -> list[str]:
    ...


@overload
def load(filename: str, reader: Literal["all"]) -> str:
    ...


@overload
def load(filename: str, reader: Callable[[Any], T]) -> T:
    ...


def load(filename: str, reader: Callable | Literal["lines", "all"]) -> Any:
    self_file = Path(filename)
    input_file = self_file.parent / f"data/{self_file.stem}.txt"
    return_: str | list[str]
    if reader == "lines":
        with open(input_file) as f:
            return_ = f.readlines()
    elif reader == "all":
        with open(input_file) as f:
            return_ = f.read()
    else:
        raise NotImplementedError
    return return_
