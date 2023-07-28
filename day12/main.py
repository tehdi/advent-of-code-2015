import logging
import argparse
import json

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


def parse_value(value, level: int) -> int:
    if type(value) is dict:
        total = add_numbers(value, level+1)
        logging.debug(f"{level}: {value} => {total}")
        return total
    if type(value) is int:
        logging.debug(f"{level}: {value} => {value}")
        return value
    if type(value) is list:
        total = sum(parse_value(item, level) for item in value)
        logging.debug(f"{level}: {value} => {total}")
        return total
    return 0


def add_numbers(data: dict, level: int) -> int:
    total = 0
    for value in data.values():
        if value == 'red':
            logging.debug('red')
            return 0
        total += parse_value(value, level)
    logging.debug(f"{level}: {data}\n =>{total}")
    return total


def part_one(input_data: list[str], args) -> None:
    total = 0
    value = ''
    for line in input_data:
        for char in line:
            if char.isdigit() or char == '-':
                value += char
            elif len(value) > 0:
                total += int(value)
                value = ''
    logging.info(f"Part One: {total}")


def part_two(input_data: list[str], args) -> None:
    data = json.loads(input_data[0])
    total = parse_value(data, 0)
    logging.info(f"Part Two: {total}")


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
