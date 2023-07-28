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

def length_without_specials(value: str) -> int:
    if len(value) == 2: return 0
    initial_length = len(value)
    unquoted_length = initial_length - 2
    value = value[1:-1] # stop the wrapper quotes from screwing up the \" sequence
    quote_escapes = unquoted_length - len(value.replace('\\"', '"'))
    backslash_escapes = unquoted_length - len(value.replace('\\\\', '\\'))
    # str_output = re.sub(regex_search_term, regex_replacement, str_input)
    ascii_characters = unquoted_length - len(re.sub(r'\\x[0-9a-f][0-9a-f]', 'a', value))
    return (initial_length - 2
        - quote_escapes
        - backslash_escapes
        - ascii_characters)

# Disregarding the whitespace in the file,
# what is the number of characters of code for string literals
# minus the number of characters in memory for the values of the strings in total
# for the entire file?
# escape sequences used:
#  \\ = single backslash
#  \" = double quote
#  \x plus two hexadecimal characters = ASCII code for a single character
# eg: "aaa\"aaa\x27" is 14 code, 8 memory: aaa"aaa'
def part_one(input_data: list[str], args) -> None:
    total_code_length = 0
    total_memory_length = 0
    for line in input_data:
        code_length = len(line)
        memory_length = length_without_specials(line)
        logging.debug(f"{line}: code = {code_length}, memory = {memory_length}")
        total_code_length += code_length
        total_memory_length += memory_length
    delta = total_code_length - total_memory_length
    logging.info(f"Part One: {total_code_length} - {total_memory_length} = {delta}")


# encode each code representation as a new string
# find the total number of characters to represent the newly encoded strings
# minus the number of characters of code in each original string literal
# "aaa\"aaa\x27" => "\"aaa\\\"aaa\\x27\""
def part_two(input_data: list[str], args) -> None:
    # add 1 '\' for each " and each \, and wrap in new ""
    characters_added = sum(2 + line.count('"') + line.count('\\') for line in input_data)
    logging.info(f"Part Two: {characters_added}")


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
