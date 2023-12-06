import argparse
import logging
import re

from utils import load as _load

logger = logging.getLogger(__name__)

prompt = """
--- Day 2: Cube Conundrum ---
You're launched high into the atmosphere! The apex of your trajectory just barely reaches the surface of a large island floating in the sky. You gently land in a fluffy pile of leaves. It's quite cold, but you don't see much snow. An Elf runs over to greet you.

The Elf explains that you've arrived at Snow Island and apologizes for the lack of snow. He'll be happy to explain the situation, but it's a bit of a walk, so you have some time. They don't get many visitors up here; would you like to play a game in the meantime?

As you walk, the Elf shows you a small bag and some cubes which are either red, green, or blue. Each time you play this game, he will hide a secret number of cubes of each color in the bag, and your goal is to figure out information about the number of cubes.

To get information, once a bag has been loaded with cubes, the Elf will reach into the bag, grab a handful of random cubes, show them to you, and then put them back in the bag. He'll do this a few times per game.

You play several games and record the information from each game (your puzzle input). Each game is listed with its ID number (like the 11 in Game 11: ...) followed by a semicolon-separated list of subsets of cubes that were revealed from the bag (like 3 red, 5 green, 4 blue).

For example, the record of a few games might look like this:

Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
In game 1, three sets of cubes are revealed from the bag (and then put back again). The first set is 3 blue cubes and 4 red cubes; the second set is 1 red cube, 2 green cubes, and 6 blue cubes; the third set is only 2 green cubes.

The Elf would first like to know which games would have been possible if the bag contained only 12 red cubes, 13 green cubes, and 14 blue cubes?

In the example above, games 1, 2, and 5 would have been possible if the bag had been loaded with that configuration. However, game 3 would have been impossible because at one point the Elf showed you 20 red cubes at once; similarly, game 4 would also have been impossible because the Elf showed you 15 blue cubes at once. If you add up the IDs of the games that would have been possible, you get 8.

Determine which games would have been possible if the bag had been loaded with only 12 red cubes, 13 green cubes, and 14 blue cubes. What is the sum of the IDs of those games?

Your puzzle answer was 2156.

The first half of this puzzle is complete! It provides one gold star: *

--- Part Two ---
The Elf says they've stopped producing snow because they aren't getting any water! He isn't sure why the water stopped; however, he can show you how to get to the water source to check it out for yourself. It's just up ahead!

As you continue your walk, the Elf poses a second question: in each game you played, what is the fewest number of cubes of each color that could have been in the bag to make the game possible?

Again consider the example games from earlier:

Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
In game 1, the game could have been played with as few as 4 red, 2 green, and 6 blue cubes. If any color had even one fewer cube, the game would have been impossible.
Game 2 could have been played with a minimum of 1 red, 3 green, and 4 blue cubes.
Game 3 must have been played with at least 20 red, 13 green, and 6 blue cubes.
Game 4 required at least 14 red, 3 green, and 15 blue cubes.
Game 5 needed no fewer than 6 red, 3 green, and 2 blue cubes in the bag.
The power of a set of cubes is equal to the numbers of red, green, and blue cubes multiplied together. The power of the minimum set of cubes in game 1 is 48. In games 2-5 it was 12, 1560, 630, and 36, respectively. Adding up these five powers produces the sum 2286.

For each game, find the minimum set of cubes that must have been present. What is the sum of the power of these sets?

Your puzzle answer was 66909.

Both parts of this puzzle are complete! They provide two gold stars: **
"""


def load() -> list[str]:
    lines = _load(__file__, reader="lines")
    return lines


def solve_part_1(lines: list[str]) -> int:
    max_red = 12
    max_green = 13
    max_blue = 14
    game_id_pattern = re.compile(r"(?:Game )(\d+)")
    n_blue_pattern = re.compile(r"(\d+)(?: blue)")
    n_red_pattern = re.compile(r"(\d+)(?: red)")
    n_green_pattern = re.compile(r"(\d+)(?: green)")
    valid_ids_sum = 0
    for line in lines:
        game_id_str, all_game_results = line.split(":")

        game_id_match = re.match(game_id_pattern, game_id_str)
        assert game_id_match is not None
        game_id = int(game_id_match.groups()[0])

        subsets = all_game_results.split(";")

        for subset in subsets:
            n_blue_match = re.search(n_blue_pattern, subset)
            if n_blue_match is not None:
                n_blue = int(n_blue_match.groups()[0])
                logger.debug("found {} blue in game {}".format(n_blue, game_id))

                if n_blue > max_blue:
                    break

            n_red_match = re.search(n_red_pattern, subset)
            if n_red_match is not None:
                n_red = int(n_red_match.groups()[0])
                logger.debug("found {} blue in game {}".format(n_red, game_id))
                if n_red > max_red:
                    break

            n_green_match = re.search(n_green_pattern, subset)
            if n_green_match is not None:
                n_green = int(n_green_match.groups()[0])
                logger.debug("found {} blue in game {}".format(n_green, game_id))
                if n_green > max_green:
                    break
        else:
            logger.debug("Adding game ID {} to sum".format(game_id))
            valid_ids_sum += game_id
    return valid_ids_sum


def solve_part_2(lines: list[str]) -> int:
    game_id_pattern = re.compile(r"(?:Game )(\d+)")
    n_blue_pattern = re.compile(r"(\d+)(?: blue)")
    n_red_pattern = re.compile(r"(\d+)(?: red)")
    n_green_pattern = re.compile(r"(\d+)(?: green)")
    final_sum = 0
    for line in lines:
        game_id_str, all_game_results = line.split(":")

        game_id_match = re.match(game_id_pattern, game_id_str)
        assert game_id_match is not None
        game_id = int(game_id_match.groups()[0])

        subsets = all_game_results.split(";")
        min_blue = 0
        min_red = 0
        min_green = 0
        for subset in subsets:
            n_blue_match = re.search(n_blue_pattern, subset)
            if n_blue_match is not None:
                n_blue = int(n_blue_match.groups()[0])
                logger.debug("found {} blue in game {}".format(n_blue, game_id))
                min_blue = max(n_blue, min_blue)

            n_red_match = re.search(n_red_pattern, subset)
            if n_red_match is not None:
                n_red = int(n_red_match.groups()[0])
                logger.debug("found {} blue in game {}".format(n_red, game_id))
                min_red = max(n_red, min_red)

            n_green_match = re.search(n_green_pattern, subset)
            if n_green_match is not None:
                n_green = int(n_green_match.groups()[0])
                logger.debug("found {} blue in game {}".format(n_green, game_id))
                min_green = max(n_green, min_green)
        game_power = min_blue * min_red * min_green
        final_sum += game_power

    return final_sum


def test_solve_part_1():
    input_ = [
        "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green",
        "Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue",
        "Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red",
        "Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red",
        "Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green",
    ]
    solution = 8
    answer = solve_part_1(input_)
    assert solution == answer, f"Answer {answer} should be {solution}"


def test_solve_part_2():
    input_ = [
        "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green",
        "Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue",
        "Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red",
        "Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red",
        "Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green",
    ]
    solution = 2286
    answer = solve_part_2(input_)
    assert solution == answer, f"Answer {answer} should be {solution}"


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", "-d", action="store_true")
    args = parser.parse_args()
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    test_solve_part_1()
    lines = load()
    part_1_solution = solve_part_1(lines)
    print(f"Part 1 solution: {part_1_solution}")

    test_solve_part_2()
    part_2_solution = solve_part_2(lines)
    print(f"Part 2 solution: {part_2_solution}")
