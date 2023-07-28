import logging
import argparse

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

location_delta = {
    '^': (0, 1),
    'v': (0, -1),
    '>': (1, 0),
    '<': (-1, 0)
}

def part_one(input_data: list[str], args) -> None:
    for line in input_data:
        location = (0, 0)
        visited = set()
        visited.add(location)
        for char in line:
            if char not in location_delta: continue
            move = location_delta[char]
            location = (
                location[0] + move[0],
                location[1] + move[1])
            visited.add(location)
        logging.debug(line)
        logging.info(len(visited))

def part_two(input_data: list[str], args) -> None:
    for line in input_data:
        visited = set()
        locations = [(0, 0), (0, 0)]
        visited.update(locations)
        santa = True
        for char in line:
            if char not in location_delta: continue
            move = location_delta[char]
            location = locations[0 if santa else 1]
            newLocation = (
                location[0] + move[0],
                location[1] + move[1])
            locations[0 if santa else 1] = newLocation
            visited.add(newLocation)
            santa = not santa
        logging.debug(f"{line} => {visited}")
        logging.info(len(visited))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '-f', '--input-file', default='input.txt')
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
