import logging
import argparse
import re

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


PROHIBITED_LETTERS = 'iol'
ORIGINALS = 'abcdefghijklmnopqrstuvwxyz'
INCREMENTED = 'bcdefghjjkmmnppqrstuvwxyza'
INCREMENTOR = str.maketrans(ORIGINALS, INCREMENTED)
PAIRS_PATTERN = re.compile(r'.*(\w)\1.*(\w)\2.*')


def increment(password: str) -> str:
    prohibited_index = min([password.index(x) for x in PROHIBITED_LETTERS if x in password], default=-1)
    if prohibited_index >= 0:
        return password[:prohibited_index] + password[prohibited_index].translate(INCREMENTOR) + ('a' * (8-prohibited_index-1))
    else:
        while password.endswith(ORIGINALS[-1]): password = password[:-1]
        password = password[:-1] + password[-1].translate(INCREMENTOR) + ('a' * (8-len(password)))
        return password

def contains_prohibited_character(password: str) -> bool:
    return any([x in password for x in PROHIBITED_LETTERS])

def contains_two_pairs(password: str) -> bool:
    return PAIRS_PATTERN.match(password)

def contains_incrementing_straight(password: str) -> bool:
    return any([password[i-3:i] in ORIGINALS for i in range(3, 9)])

def is_valid(password: str) -> bool:
    return (not contains_prohibited_character(password)
        and contains_two_pairs(password)
        and contains_incrementing_straight(password))


# make a new password by incrementing until you find something that matches all the rules
# must be exactly eight lowercase letters
# must contain one increasing straight of at least three letters (eg. abc, bcd, cde, xyz)
# may not contain i, o, or l
# must contain at least two different, non-overlapping pairs of letters (eg. aa, bb, zz)
# incrementing works like this: xx -> xy -> xz -> ya -> yb
# abcdefgh -> abcdffaa
# ghijklmn -> ghjaabcc
def part_one(input_data: list[str], args) -> list[str]:
    next_passwords = []
    for line in input_data:
        password = increment(line)
        while not is_valid(password):
            # logging.debug(password)
            password = increment(password)
        next_passwords.append(password)
    logging.info("Part One:")
    for i in range(len(input_data)):
        logging.info(f"{input_data[i]} -> {next_passwords[i]}")
    return next_passwords


# Santa's password expired again. What's the next one?
def part_two(input_data: list[str], args) -> None:
    next_password = part_one(input_data, args)
    next_next_password = part_one(next_password, args)
    logging.info(f"Part Two: {next_next_password}")


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
