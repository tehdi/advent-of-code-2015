import logging
import argparse
import re
from collections import defaultdict

def configure_logging(verbose, output_file):
    log_level = logging.DEBUG if verbose else logging.INFO
    if output_file is None:
        logging.basicConfig(
            format='%(message)s',
            level=log_level
        )
    else:
        logging.basicConfig(
            format='%(message)s',
            level=log_level,
            filename=output_file,
            filemode='w'
        )

def turn_on(coords: tuple[int, int], lit_lights: set[tuple[int, int]]) -> None:
    lit_lights.add(coords)

def turn_off(coords: tuple[int, int], lit_lights: set[tuple[int, int]]) -> None:
    if coords in lit_lights: lit_lights.remove(coords)

def toggle(coords: tuple[int, int], lit_lights: set[tuple[int, int]]) -> None:
    if coords in lit_lights: lit_lights.remove(coords)
    else: lit_lights.add(coords)

def increase_brightness(coords: tuple[int, int], lights: dict[tuple[int, int], int]) -> None:
    lights[coords] += 1

def decrease_brightness(coords: tuple[int, int], lights: dict[tuple[int, int], int]) -> None:
    new_value = lights[coords] - 1
    # don't let it go below 0
    lights[coords] = max(new_value, 0)

def double_increase_brightness(coords: tuple[int, int], lights: dict[tuple[int, int], int]) -> None:
    lights[coords] += 2

actions = {
    'turn on': (turn_on, increase_brightness),
    'turn off': (turn_off, decrease_brightness),
    'toggle': (toggle, double_increase_brightness)
}

def part_one(input_data: list[str], args) -> None:
    line_pattern = re.compile('(.+) (\d+),(\d+) through (\d+),(\d+)')
    lit_lights = set()
    for line in input_data:
        m = line_pattern.match(line)
        action = actions[m.group(1)][0]
        start_x = int(m.group(2))
        start_y = int(m.group(3))
        end_x = int(m.group(4))
        end_y = int(m.group(5))
        for x in range(start_x, end_x+1):
            for y in range(start_y, end_y+1):
                action((x, y), lit_lights)
    logging.info(f"Part One: {len(lit_lights)}")


def part_two(input_data: list[str], args) -> None:
    line_pattern = re.compile('(.+) (\d+),(\d+) through (\d+),(\d+)')
    lights = defaultdict(int)
    for line in input_data:
        m = line_pattern.match(line)
        action = actions[m.group(1)][1]
        start_x = int(m.group(2))
        start_y = int(m.group(3))
        end_x = int(m.group(4))
        end_y = int(m.group(5))
        for x in range(start_x, end_x+1):
            for y in range(start_y, end_y+1):
                action((x, y), lights)
    logging.info(f"Part Two: {sum(lights.values())}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '-f', '--input-file')
    parser.add_argument('-o', '--output-file', default=None)
    parser.add_argument('-v', '--verbose', '--debug', default=False, action='store_true')
    parser.add_argument('-p', '--part', type=int, default=1)
    args = parser.parse_args()
    configure_logging(args.verbose, args.output_file)

    filename = args.input_file
    with open(filename) as input_file:
        input_data = [line.rstrip('\n') for line in input_file]
    if args.part == 1: part_one(input_data, args)
    elif args.part == 2: part_two(input_data, args)
