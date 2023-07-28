import logging
import argparse
import hashlib

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

def part_one(input_value: str, args) -> None:
    logging.info(f"Part One: {input_value}")
    suffix = 0
    while True:
        value = input_value + str(suffix)
        hashed = hashlib.md5(value.encode(encoding='UTF-8')).hexdigest()
        if hashed[:5] == '00000':
            logging.info(f"{suffix} => {hashed}")
            break
        suffix += 1


def part_two(input_value: str, args) -> None:
    logging.info(f"Part Two: {input_value}")
    suffix = 0
    while True:
        value = input_value + str(suffix)
        hashed = hashlib.md5(value.encode(encoding='UTF-8')).hexdigest()
        if suffix % 1000000 == 0: logging.debug(f"{suffix} => {hashed}")
        if hashed[:6] == '000000':
            logging.info(f"{suffix} => {hashed}")
            break
        suffix += 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output-file', default=None)
    parser.add_argument('-i', '--input-value', type=str, default=None)
    parser.add_argument('-v', '--verbose', '--debug', default=False, action='store_true')
    parser.add_argument('-p', '--part', type=int, default=1)
    args = parser.parse_args()
    configure_logging(args.verbose, args.output_file)

    input_value = args.input_value or 'yzbqklnj'
    if args.part == 1: part_one(input_value, args)
    elif args.part == 2: part_two(input_value, args)
