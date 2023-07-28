import logging
import argparse
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


def find_factors(number):
    factors = set([1, number])
    for i in range(int(number**0.5), 1, -1):
        if number % i == 0:
            factors.add(i)
            factors.add(number // i)
    return factors


# There are infinitely many Elves, numbered starting with 1.
# Each Elf delivers presents to a house if the house's number is divisible by the Elf's number.
# Each Elf delivers presents equal to ten times his or her number at each house.
# What is the lowest house number to get at least as many presents as the number in your puzzle input?
def part_one(target_gifts: int, args) -> None:
    target_gifts = int(target_gifts / 10)
    gifts = 0
    house_number = 0
    while gifts < target_gifts:
        house_number += 1
        elf_visitors = find_factors(house_number)
        gifts = sum(elf_visitors)
        if args.logging_interval > 0 and house_number % args.logging_interval == 0:
            logging.debug(f"H{house_number}: G{gifts*10}")

    logging.info(f"Part One: T {target_gifts*10} => H {house_number}")


# each Elf will stop after delivering presents to 50 houses
# but will deliver presents equal to eleven times their number at each house
# What is the new lowest house number to get at least as many presents as the number in your puzzle input?
def part_two(target_gifts: int, args) -> None:
    max_deliveries_per_elf = 50
    gifts_per_elf_number = 11
    gifts_delivered = defaultdict(int)
    gifts = 0
    house_number = 0
    while gifts < target_gifts:
        gifts = 0
        house_number += 1
        elf_visitors = find_factors(house_number)
        for e in elf_visitors:
            if gifts_delivered[e] < max_deliveries_per_elf:
                gifts_delivered[e] += 1
                gifts += e * gifts_per_elf_number
        if args.logging_interval > 0 and house_number % args.logging_interval == 0:
            logging.debug(f"H{house_number}: G{gifts}")
    logging.info(f"Part Two: T {target_gifts} => H {house_number}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input-file', default=None)
    parser.add_argument('-o', '--output-file', default=None)
    parser.add_argument('-v', '--verbose', default=False, action='store_true')
    parser.add_argument('-p', '--part', type=int, default=1)
    parser.add_argument('-l', '--logging-interval', type=int, default=0)
    parser.add_argument('-t', '--target-gifts', type=int, default=None)
    args = parser.parse_args()
    configure_logging(args.verbose, args.output_file)

    filename = args.input_file
    with open(filename) as input_file:
        input_data = [int(line.rstrip('\n')) for line in input_file]
    target_gifts = input_data[0] if args.target_gifts is None else args.target_gifts
    if args.part == 1: part_one(target_gifts, args)
    elif args.part == 2: part_two(target_gifts, args)
