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

def count_characters(data: str) -> list[tuple[int, str]]:
    return [(1, char) for char in data]

def merge_adjacent(data: list[tuple[int, str]]) -> list[tuple[int, str]]:
    last = data[0]
    merged = []
    for count, char in data[1:]:
        if char == last[1]:
            last = (last[0] + count, char)
        else:
            merged.append(last)
            last = (count, char)
    merged.append(last)
    return merged

def flatten(data: list[tuple[int, str]]) -> list[tuple[int, str]]:
    return ''.join(str(count) + char for count, char in data)

# 1 -> 11
# 11 -> 21
# 21 -> 1211
# 1211 -> 111221
# 111221 -> 312211
def part_one(input_data: list[str], args) -> None:
    data = input_data[0]
    for _ in range(args.rounds):
        data = count_characters(data)
        data = merge_adjacent(data)
        data = flatten(data)
    logging.info(f"Part One: {len(data)}")

def part_two(input_data: list[str], args) -> None:
    logging.info(f"Part Two is just more rounds of part 1")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '-f', '--input-file', default=None)
    parser.add_argument('-o', '--output-file', default=None)
    parser.add_argument('-v', '--verbose', '--debug', default=False, action='store_true')
    parser.add_argument('-p', '--part', type=int, default=1)
    parser.add_argument('-r', '--rounds', type=int, required=True)
    args = parser.parse_args()
    configure_logging(args.verbose, args.output_file)

    filename = args.input_file
    with open(filename) as input_file:
        input_data = [line.rstrip('\n') for line in input_file]
    if args.part == 1: part_one(input_data, args)
    elif args.part == 2: part_two(input_data, args)
