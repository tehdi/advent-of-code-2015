import logging
import argparse
from itertools import product

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

ON = '#'
OFF = '.'

def count_on_neighbours(position, lights):
    row = position[0]
    col = position[1]
    count = 0
    for (r, c) in product([row-1, row, row+1], [col-1, col, col+1]):
        if (r, c) == position: continue
        if lights.get((r, c), OFF) == ON: count += 1
    return count

def get_new_state(light, on_neighbour_count):
    if light == ON and on_neighbour_count in [2, 3]: return ON
    if light == OFF and on_neighbour_count == 3: return ON
    return OFF

def step(lights):
    temp = {}
    for (p, l) in lights.items():
        on_neighbour_count = count_on_neighbours(p, lights)
        temp[p] = get_new_state(l, on_neighbour_count)
    return temp

def print_lights(lights, max_r, max_c):
    for r in range(max_r+1):
        line = ''
        for c in range(max_c+1):
            line += lights[(r, c)]
        logging.debug(line)
    logging.debug('')

# Game of Life.
# Input: A # means "on", and a . means "off"
# Lights on the edge of the grid might have fewer than eight neighbors;
# the missing ones always count as "off".
# A light which is on stays on when 2 or 3 neighbors are on, and turns off otherwise.
# A light which is off turns on if exactly 3 neighbors are on, and stays off otherwise.
# In your grid of 100x100 lights, given your initial configuration,
# how many lights are on after 100 steps?
def part_one(input_data: list[str], args) -> None:
    lights = {}
    for line_index,line in enumerate(input_data):
        for char_index,char in enumerate(line):
            lights[(line_index, char_index)] = char
    for s in range(args.steps):
        lights = step(lights)
    logging.info(f"Part One: {list(lights.values()).count(ON)}")


# four lights, one in each corner, are stuck on and can't be turned off
# now how many are on after 100 steps?
def part_two(input_data: list[str], args) -> None:
    lights = {}
    max_r = 0
    max_c = 0
    for row_index,line in enumerate(input_data):
        if max_c == 0: max_c = len(line) - 1
        max_r = max(max_r, row_index)
        for col_index,char in enumerate(line):
            lights[(row_index, col_index)] = char
    corners = set([(0, 0), (0, max_c), (max_r, 0), (max_r, max_c)])
    for c in corners: lights[c] = ON
    for s in range(args.steps):
        lights = step(lights)
        for c in corners: lights[c] = ON
        # print_lights(lights, max_r, max_c)
    logging.info(f"Part Two: {list(lights.values()).count(ON)}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input-file', default=None)
    parser.add_argument('-o', '--output-file', default=None)
    parser.add_argument('-v', '--verbose', default=False, action='store_true')
    parser.add_argument('-p', '--part', type=int, default=1)
    parser.add_argument('-s', '--steps', type=int, default=100)
    args = parser.parse_args()
    configure_logging(args.verbose, args.output_file)

    filename = args.input_file
    with open(filename) as input_file:
        input_data = [line.rstrip('\n') for line in input_file]
    if args.part == 1: part_one(input_data, args)
    elif args.part == 2: part_two(input_data, args)
