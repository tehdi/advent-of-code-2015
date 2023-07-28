import logging
import argparse
from collections import defaultdict, deque

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

def parse_input(input_data) -> dict:
    destination_distances = defaultdict(dict) # { str destination: { str destination: int distance}}
    for line in input_data:
        data = line.split()
        origin = data[0]
        destination = data[2]
        distance = int(data[4])
        destination_distances[origin][destination] = distance
        destination_distances[destination][origin] = distance
    return destination_distances

def prepare_paths(destination_distances: dict[str, dict[str, int]]) -> deque:
    paths = deque()
    for destination in destination_distances:
        paths.append({
            'visited': [ destination ],
            'remaining': [
                (name, distance)
                for name, distance in destination_distances[destination].items()],
            'distance': 0 })
    return paths

def build_paths_from_here(path, destination_distances) -> deque:
    paths = deque()
    for name, distance in path['remaining']:
        paths.append({
            'visited': path['visited'] + [name],
            'remaining': [
                (n, d)
                for n, d in destination_distances[name].items()
                if n not in path['visited']],
            'distance': path['distance'] + distance })
    return paths

def current_too_high(best: int, current: int) -> bool:
    return best is not None and best < current

def current_too_low(best: int, current: int) -> bool:
    return False

def is_current_lower(current: int, best: int) -> bool:
    return best is None or current < best

def is_current_higher(current: int, best: int) -> bool:
    return best is None or current > best

def find_best_path(
            destination_distances: dict[str, dict[str, int]],
            should_prune_func, is_better_func
        ) -> tuple[list[str], int]:
    paths = prepare_paths(destination_distances)
    best = { 'path': None, 'distance': None }
    while len(paths) > 0:
        path = paths.popleft()
        if should_prune_func(best['distance'], path['distance']):
            continue
        if len(path['remaining']) == 0:
            if is_better_func(path['distance'], best['distance']):
                best['path'] = path['visited']
                best['distance'] = path['distance']
        paths.extendleft(build_paths_from_here(path, destination_distances))
    return best


# What's the shortest distance you can travel to visit each destination exactly once?
# You can start and end wherever you want.
def part_one(input_data: list[str], args) -> None:
    destination_distances = parse_input(input_data)
    shortest = find_best_path(destination_distances, current_too_high, is_current_lower)
    logging.info(f"Part One: {shortest['distance']} via path {shortest['path']}")


# To show off, Santa wants the longest route instead.
def part_two(input_data: list[str], args) -> None:
    destination_distances = parse_input(input_data)
    longest = find_best_path(destination_distances, current_too_low, is_current_higher)
    logging.info(f"Part Two: {longest['distance']} via path {longest['path']}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '-f', '--input-file', default=None)
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
