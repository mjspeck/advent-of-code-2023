import re
from itertools import product
from typing import Sequence

from utils import load as _load

prompt = """--- Day 3: Gear Ratios ---
You and the Elf eventually reach a gondola lift station; he says the gondola lift will take you up to the water source, but this is as far as he can bring you. You go inside.

It doesn't take long to find the gondolas, but there seems to be a problem: they're not moving.

"Aaah!"

You turn around to see a slightly-greasy Elf with a wrench and a look of surprise. "Sorry, I wasn't expecting anyone! The gondola lift isn't working right now; it'll still be a while before I can fix it." You offer to help.

The engineer explains that an engine part seems to be missing from the engine, but nobody can figure out which one. If you can add up all the part numbers in the engine schematic, it should be easy to work out which part is missing.

The engine schematic (your puzzle input) consists of a visual representation of the engine. There are lots of numbers and symbols you don't really understand, but apparently any number adjacent to a symbol, even diagonally, is a "part number" and should be included in your sum. (Periods (.) do not count as a symbol.)

Here is an example engine schematic:

467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
In this schematic, two numbers are not part numbers because they are not adjacent to a symbol: 114 (top right) and 58 (middle right). Every other number is adjacent to a symbol and so is a part number; their sum is 4361.

Of course, the actual engine schematic is much larger. What is the sum of all of the part numbers in the engine schematic?

Your puzzle answer was 539590.

The first half of this puzzle is complete! It provides one gold star: *

--- Part Two ---
The engineer finds the missing part and installs it in the engine! As the engine springs to life, you jump in the closest gondola, finally ready to ascend to the water source.

You don't seem to be going very fast, though. Maybe something is still wrong? Fortunately, the gondola has a phone labeled "help", so you pick it up and the engineer answers.

Before you can explain the situation, she suggests that you look out the window. There stands the engineer, holding a phone in one hand and waving with the other. You're going so slowly that you haven't even left the station. You exit the gondola.

The missing part wasn't the only issue - one of the gears in the engine is wrong. A gear is any * symbol that is adjacent to exactly two part numbers. Its gear ratio is the result of multiplying those two numbers together.

This time, you need to find the gear ratio of every gear and add them all up so that the engineer can figure out which gear needs to be replaced.

Consider the same engine schematic again:

467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
In this schematic, there are two gears. The first is in the top left; it has part numbers 467 and 35, so its gear ratio is 16345. The second gear is in the lower right; its gear ratio is 451490. (The * adjacent to 617 is not a gear because it is only adjacent to one part number.) Adding up all of the gear ratios produces 467835.

What is the sum of all of the gear ratios in your engine schematic?

Your puzzle answer was 80703636.

Both parts of this puzzle are complete! They provide two gold stars: **
"""


def load() -> list[str]:
    lines = _load(__file__, reader="lines")
    return lines


def _check_line(
    line: str,
    num_span: tuple[int, int],
    check_ahead: bool,
    check_behind: bool,
    normal_symbol: str = ".",
) -> bool:
    if check_behind:
        start = num_span[0] - 1
    else:
        start = num_span[0]

    if check_ahead:
        end = num_span[1]
    else:
        end = num_span[1] - 1
    for char in line[start : end + 1]:
        if char != normal_symbol:
            return True
    return False


def _is_number_adjacent_to_symbol(
    number: re.Match,
    above_line: str | None,
    current_line: str,
    below_line: str | None,
    normal_symbol: str = ".",
) -> bool:
    """Determine if a number is adjacent to a non-period symbol.

    Parameters
    ----------
    number : re.Match
        match object for number
    above_line : str | None
        string for line above number
    current_line : str
        string for line that number is in
    below_line : str | None
        string for line below number

    Returns
    -------
    bool
        Answer
    """

    span = number.span()
    check_behind = bool(span[0])  # False if 0
    check_ahead = span[1] != len(current_line) - 1

    if check_behind:
        if current_line[span[0] - 1] != normal_symbol:
            return True
    if check_ahead:
        if current_line[span[1]] != normal_symbol:
            return True
    if above_line:
        above_has_symbol = _check_line(above_line, span, check_ahead, check_behind)
        if above_has_symbol:
            return True
    if below_line:
        below_has_symbol = _check_line(below_line, span, check_ahead, check_behind)
        if below_has_symbol:
            return True
    return False


def solve_part_1(lines: Sequence[str]) -> int:
    pattern = re.compile(r"\d+")
    part_numbers = []
    n_lines = len(lines)
    for ind in range(n_lines):
        if ind == 0:
            above_line = None
        else:
            above_line = lines[ind - 1]
        current_line = lines[ind]

        if ind == n_lines - 1:
            below_line = None
        else:
            below_line = lines[ind + 1]

        numbers_in_current_line = re.finditer(pattern, current_line)
        for number in numbers_in_current_line:
            is_part_number = _is_number_adjacent_to_symbol(
                number, above_line, current_line, below_line
            )
            if is_part_number:
                part_numbers.append(int(number.group()))
    return sum(part_numbers)


def test_solve_part_1():
    input_ = (
        "467..114..\n"
        "...*......\n"
        "..35..633.\n"
        "......#...\n"
        "617*......\n"
        ".....+.58.\n"
        "..592.....\n"
        "......755.\n"
        "...$.*....\n"
        ".664.598..\n"
    ).split("\n")
    solution = 4361
    answer = solve_part_1(input_)
    assert solution == answer, f"Answer {answer} should be {solution}"


def _get_adjacent_numbers(
    coords: tuple[int, int],
    numbers: dict[tuple[int, int], re.Match],
    n_lines: int,
    line_length: int,
) -> list[int]:
    if coords[0] == 0:
        check_behind = False
    else:
        check_behind = True

    if coords[0] == line_length - 1:
        check_ahead = False
    else:
        check_ahead = True

    if coords[1] == 0:
        check_above = False
    else:
        check_above = True

    if coords[1] == n_lines - 1:
        check_below = False
    else:
        check_below = True

    locations_to_check: list[tuple[int, int]] = []

    if check_above:
        locations_to_check.append((coords[0], coords[1] - 1))
    if check_below:
        locations_to_check.append((coords[0], coords[1] + 1))

    if check_behind:
        locations_to_check.append((coords[0] - 1, coords[1]))
        if check_above:
            locations_to_check.append((coords[0] - 1, coords[1] - 1))
        if check_below:
            locations_to_check.append((coords[0] - 1, coords[1] + 1))
    if check_ahead:
        locations_to_check.append((coords[0] + 1, coords[1]))
        if check_above:
            locations_to_check.append((coords[0] + 1, coords[1] - 1))
        if check_below:
            locations_to_check.append((coords[0] + 1, coords[1] + 1))

    adjacent_numbers: list[int] = []
    for location in locations_to_check:
        if location in numbers:
            num = int(numbers[location].group())
            adjacent_numbers.append(num)

    return list(set(adjacent_numbers))


def solve_part_2(lines: Sequence[str]) -> int:
    num_pattern = re.compile(r"\d+")
    n_lines = len(lines)
    line_length = len(lines[0])

    numbers: dict[tuple[int, int], re.Match] = {}
    for i, line in enumerate(lines):
        numbers_in_line = list(re.finditer(num_pattern, line))
        for number in numbers_in_line:
            span = number.span()
            all_coords = product(range(*span), [i])
            for coords in all_coords:
                numbers[coords] = number
    # numbers = {i: list(re.finditer(num_pattern, line)) for i, line in enumerate(lines)}
    gear_ratios = 0
    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            if char == "*":
                coords = (j, i)
                adjacent_numbers = _get_adjacent_numbers(
                    coords, numbers, n_lines, line_length
                )
                if len(adjacent_numbers) == 2:
                    gear_ratios += adjacent_numbers[0] * adjacent_numbers[1]

    return gear_ratios


def test_solve_part_2():
    input_ = (
        "467..114..\n"
        "...*......\n"
        "..35..633.\n"
        "......#...\n"
        "617*......\n"
        ".....+.58.\n"
        "..592.....\n"
        "......755.\n"
        "...$.*....\n"
        ".664.598..\n"
    ).split("\n")
    solution = 467835
    answer = solve_part_2(input_)
    assert solution == answer, f"Answer {answer} should be {solution}"


if __name__ == "__main__":
    test_solve_part_1()
    lines = load()
    part_1_solution = solve_part_1(lines)
    print(f"Part 1 solution: {part_1_solution}")

    test_solve_part_2()
    part_2_solution = solve_part_2(lines)
    print(f"Part 2 solution: {part_2_solution}")
