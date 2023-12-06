import re

from utils import load as _load

prompt = """--- Day 1: Trebuchet?! ---
Something is wrong with global snow production, and you've been selected to take a look. The Elves have even given you a map; on it, they've used stars to mark the top fifty locations that are likely to be having problems.

You've been doing this long enough to know that to restore snow operations, you need to check all fifty stars by December 25th.

Collect stars by solving puzzles. Two puzzles will be made available on each day in the Advent calendar; the second puzzle is unlocked when you complete the first. Each puzzle grants one star. Good luck!

You try to ask why they can't just use a weather machine ("not powerful enough") and where they're even sending you ("the sky") and why your map looks mostly blank ("you sure ask a lot of questions") and hang on did you just say the sky ("of course, where do you think snow comes from") when you realize that the Elves are already loading you into a trebuchet ("please hold still, we need to strap you in").

As they're making the final adjustments, they discover that their calibration document (your puzzle input) has been amended by a very young Elf who was apparently just excited to show off her art skills. Consequently, the Elves are having trouble reading the values on the document.

The newly-improved calibration document consists of lines of text; each line originally contained a specific calibration value that the Elves now need to recover. On each line, the calibration value can be found by combining the first digit and the last digit (in that order) to form a single two-digit number.

For example:

g1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
In this example, the calibration values of these four lines are 12, 38, 15, and 77. Adding these together produces 142.

Consider your entire calibration document. What is the sum of all of the calibration values?

Your puzzle answer was 54081.

The first half of this puzzle is complete! It provides one gold star: *

--- Part Two ---
Your calculation isn't quite right. It looks like some of the digits are actually spelled out with letters: one, two, three, four, five, six, seven, eight, and nine also count as valid "digits".

Equipped with this new information, you now need to find the real first and last digit on each line. For example:

two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
In this example, the calibration values are 29, 83, 13, 24, 42, 14, and 76. Adding these together produces 281.

What is the sum of all of the calibration values?

Your puzzle answer was 54649.

Both parts of this puzzle are complete! They provide two gold stars: **
"""


def load() -> list[str]:
    lines = _load(__file__, reader="lines")
    return lines


def solve_part_1(lines: list[str]) -> int:
    total = 0
    pattern = re.compile(r"\d")
    for line in lines:
        numbers = re.findall(pattern, line)
        first = numbers[0]
        last = numbers[-1]
        total += int(f"{first}{last}")
    return total


def test_solve_part_1():
    input_data = [
        "g1abc2",
        "pqr3stu8vwx",
        "a1b2c3d4e5f",
        "treb7uchet",
    ]
    answer = solve_part_1(input_data)
    solution = 142
    try:
        assert solution == answer
    except AssertionError:
        print(f"Answer {answer} should be {solution}")


def solve_part_2(lines: list[str]) -> int:
    pattern = re.compile(r"(?=(\d|one|two|three|four|five|six|seven|eight|nine))")
    number_maps = {
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9",
    }
    total = 0
    for line in lines:
        matches = re.findall(pattern, line)
        first = matches[0]
        last = matches[-1]
        if first in number_maps:
            first = number_maps[first]
        if last in number_maps:
            last = number_maps[last]
        total += int(f"{first}{last}")
    return total


def test_solve_part_2():
    input_data = [
        "two1nine",
        "eightwothree",
        "abcone2threexyz",
        "xtwone3four",
        "4nineeightseven2",
        "zoneight234",
        "7pqrstsixteen",
    ]
    answer = solve_part_2(input_data)
    solution = 281
    try:
        assert solution == answer
    except AssertionError:
        print(f"Answer {answer} should be {solution}")


if __name__ == "__main__":
    test_solve_part_1()
    lines = load()
    part_1_solution = solve_part_1(lines)
    print(f"Part 1 solution: {part_1_solution}")
    test_solve_part_2()
    part_2_solution = solve_part_2(lines)
    print(f"Part 2 solution: {part_2_solution}")
