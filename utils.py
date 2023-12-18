from __future__ import annotations

from enum import IntEnum
from pathlib import Path
from typing import TYPE_CHECKING, Callable, overload

if TYPE_CHECKING:
    from typing import Any, Callable, Literal

FilePath = Path | str


class Part(IntEnum):
    ONE = 1
    TWO = 2


@overload
def load(filename: FilePath, reader: Literal["lines"]) -> list[str]:
    ...


@overload
def load(filename: FilePath, reader: Literal["all"]) -> str:
    ...


@overload
def load[T](filename: FilePath, reader: Callable[[FilePath], T]) -> T:
    ...


def load(
    filename: FilePath, reader: Callable[[FilePath], Any] | Literal["lines", "all"]
) -> Any:
    """Load data for challenge.

    This function assumes that the data file will have the same name as the source code file
    except for a .txt extension instead of a .py and that it will live in a directory called
    data that is in the same directory as teh source code file.

    Parameters
    ----------
    filename : FilePath
        The name of the source code file.
    reader : Callable[[FilePath], Any] | Literal["lines", "all"]
        How to read the data file. If "lines," will use f.readlines. If "all." will use f.read().
        If a callable, will use that function to read the data.

    Returns
    -------
    Any
        _description_
    """
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
        return_ = reader(input_file)
    return return_


def test_solve[
    T
](input_: T, solver: Callable[[T], int], part: Part, solution: int) -> None:
    answer = solver(input_)
    assert solution == answer, f"Answer {answer} should be {solution} for part {part}"
    print(f"Test for part {part} passed")


def solve[T](input_: T, solver: Callable[[T], int], part: Part) -> None:
    solution = solver(input_)
    print(f"Part {part} solution: {solution}")
