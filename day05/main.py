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

naughty_sequences = set([ 'ab', 'cd', 'pq', 'xy'])
vowels = 'aeiou'

def contains_naughty_sequence(value: str) -> bool:
    return any(sequence in value for sequence in naughty_sequences)

def contains_double_letters(value: str) -> bool:
    return any(value[i] == value[i-1] for i in range(1, len(value)))

def count_vowels(value: str) -> int:
    return sum(value.count(vowel) for vowel in vowels)

def part_one(input_data: list[str], args) -> None:
    nice_strings = 0
    for line in input_data:
        if contains_naughty_sequence(line): continue
        if not contains_double_letters(line): continue
        if count_vowels(line) < 3: continue
        nice_strings += 1
    logging.info(f"Part One: {nice_strings}")


def contains_repeated_pair(value: str) -> bool:
    return any(value.count(value[i-2:i]) >= 2 for i in range(2, len(value)))

def contains_split_duplicate(value: str) -> bool:
    return any(value[i-2] == value[i] for i in range(2, len(value)))

def part_two(input_data: list[str], args) -> None:
    nice_strings = 0
    for line in input_data:
        if not contains_repeated_pair(line): continue
        if not contains_split_duplicate(line): continue
        nice_strings += 1
    logging.info(f"Part Two: {nice_strings}")


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
