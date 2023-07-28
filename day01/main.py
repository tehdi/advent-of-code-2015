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

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '-f', '--input-file', default='input.txt')
    parser.add_argument('-o', '--output-file', default=None)
    parser.add_argument('-v', '--verbose', '--debug', default=False, action='store_true')
    args = parser.parse_args()
    configure_logging(args.verbose, args.output_file)

    filename = args.input_file
    change = { '(': 1, ')': -1 }
    floor = 0
    basement_found = False
    with open(filename) as input_file:
        for line in input_file:
            for char_index,char in enumerate(line):
                floor += change.get(char, 0)
                if floor == -1 and not basement_found:
                    print(f"Entering basement at position {char_index+1}")
                    basement_found = True
    print(floor)
