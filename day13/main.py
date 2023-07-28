import logging
import argparse
import itertools
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

def unpack_data(data):
    people = set()
    happiness_pairs = defaultdict(int)
    for line in data:
        # Carol would gain 24 happiness units by sitting next to David.
        # David would gain 99 happiness units by sitting next to Carol.
        # => CarolDavid 123
        data = line.rstrip('.').split()
        pair = ''.join(sorted([data[0], data[-1]]))
        people.add(data[0])
        people.add(data[-1])
        happiness = int(data[3]) * (1 if data[2] == 'gain' else -1)
        happiness_pairs[pair] += happiness
    return (people, happiness_pairs)

def find_happiest_arrangement(people, happiness_pairs):
    leader = people.pop()
    staging = set()
    for ps in itertools.permutations(people):
        if (ps[::-1] not in staging): staging.add(ps)
    arrangements = set()
    for ss in staging:
        arrangements.add(tuple([leader] + [s for s in ss]))
    max_happiness = 0
    happiest_arrangement = None
    for arrangement in arrangements:
        logging.debug(arrangement)
        total_happiness = 0
        for i in range(len(arrangement)):
            one = arrangement[i]
            two = arrangement[i-1]
            pair = ''.join(sorted([one, two]))
            happiness = happiness_pairs[pair]
            total_happiness += happiness
            if total_happiness > max_happiness:
                max_happiness = total_happiness
                happiest_arrangement = arrangement
            logging.debug(f"{one} next to {two} yields {happiness} happiness / {max_happiness} max found so far")
    return (max_happiness, happiest_arrangement)


# AliceBob +54
# BobAlice +83
# => AliceBob +137
# ['Alice', 'Bob', 'Carol', ...]
# => AliceBob, BobCarol, ...
# because this is a circle, ABCD is the same as BCDA, CDAB, and DABC
# plus we can go around in either direction so ^ also matches ADCB, DCBA, etc
def part_one(input_data: list[str], args) -> None:
    (people, happiness_pairs) = unpack_data(input_data)
    (max_happiness, happiest_arrangement) = find_happiest_arrangement(people, happiness_pairs)
    # expected max happiness for test input: 330
    # max happiness for real input: 618
    logging.info(f"Part One: {max_happiness} => {happiest_arrangement}")


# Forgot to seat myself. I'm worth 0 happiness regardless of who I sit next to.
def part_two(input_data: list[str], args) -> None:
    (people, happiness_pairs) = unpack_data(input_data)
    for person in people:
        pair = ''.join(sorted(['Me', person]))
        happiness_pairs[pair] = 0
    people.add('Me')
    (max_happiness, happiest_arrangement) = find_happiest_arrangement(people, happiness_pairs)
    # max happiness for real input: 601
    # vs 618 without me :(
    logging.info(f"Part Two: {max_happiness} => {happiest_arrangement}")


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
