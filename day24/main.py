import logging
import argparse
import itertools
import math


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


def find_min_entanglement(package_weights, target_weight):
    valid_groups = set()
    for count in range(len(package_weights)):
        combinations = itertools.combinations(package_weights, count+1)
        for combination in combinations:
            if sum(combination) == target_weight:
                valid_groups.add(combination)
        if len(valid_groups) > 0: break
    return sorted(math.prod(g) for g in valid_groups)[0]


def part_one(package_weights, args) -> None:
    target_weight = int(sum(package_weights) / 3)
    min_entanglement = find_min_entanglement(package_weights, target_weight)
    logging.info(f"Part One: {min_entanglement}")


def part_two(package_weights, args) -> None:
    target_weight = int(sum(package_weights) / 4)
    min_entanglement = find_min_entanglement(package_weights, target_weight)
    logging.info(f"Part Two: {min_entanglement}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input-file', default=None)
    parser.add_argument('-o', '--output-file', default=None)
    parser.add_argument('-v', '--verbose', default=False, action='store_true')
    parser.add_argument('-p', '--part', type=int, default=1)
    args = parser.parse_args()
    configure_logging(args.verbose, args.output_file)

    filename = args.input_file
    with open(filename) as input_file:
        input_data = [int(line.rstrip('\n')) for line in input_file]
    if args.part == 1: part_one(input_data, args)
    elif args.part == 2: part_two(input_data, args)
