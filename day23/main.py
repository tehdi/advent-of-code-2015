import logging
import argparse
import re
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

hlf_pattern = re.compile(r'hlf (\w)')
tpl_pattern = re.compile(r'tpl (\w)')
inc_pattern = re.compile(r'inc (\w)')
jmp_pattern = re.compile(r'jmp ([+-]\d+)')
jie_pattern = re.compile(r'jie (\w), ([+-]\d+)')
jio_pattern = re.compile(r'jio (\w), ([+-]\d+)')

def apply_hlf(instruction, register_values):
    logging.debug(f"HLF {instruction}")
    m = hlf_pattern.match(instruction)
    register = m.group(1)
    register_values[register] /= 2

def apply_tpl(instruction, register_values):
    logging.debug(f"TPL {instruction}")
    m = tpl_pattern.match(instruction)
    register = m.group(1)
    register_values[register] *= 3

def apply_inc(instruction, register_values):
    logging.debug(f"INC {instruction}")
    m = inc_pattern.match(instruction)
    register = m.group(1)
    register_values[register] += 1

def apply_jmp(instruction):
    logging.debug(f"JMP {instruction}")
    m = jmp_pattern.match(instruction)
    return int(m.group(1))

def apply_jie(instruction, register_values):
    logging.debug(f"JIE {instruction}")
    m = jie_pattern.match(instruction)
    register = m.group(1)
    if register_values[register] % 2 == 0: return int(m.group(2))
    return 1

def apply_jio(instruction, register_values):
    logging.debug(f"JIO {instruction}")
    m = jio_pattern.match(instruction)
    register = m.group(1)
    if register_values[register] == 1: return int(m.group(2))
    return 1


def run(instructions, register_values, register_wanted):
    index = 0
    while index < len(instructions):
        instruction = instructions[index]
        if instruction.startswith('hlf'):
            apply_hlf(instruction, register_values)
            index += 1
        elif instruction.startswith('tpl'):
            apply_tpl(instruction, register_values)
            index += 1
        elif instruction.startswith('inc'):
            apply_inc(instruction, register_values)
            index += 1
        elif instruction.startswith('jmp'):
            index += apply_jmp(instruction)
        elif instruction.startswith('jie'):
            index += apply_jie(instruction, register_values)
        elif instruction.startswith('jio'):
            index += apply_jio(instruction, register_values)
        logging.debug(register_values)
    return register_values[register_wanted]


# What is the value in register b when the program in your puzzle input is finished executing?
# The program exits when it tries to run an instruction beyond the ones defined.
def part_one(instructions: list[str], args) -> None:
    register_values = defaultdict(int)
    value = run(instructions, register_values, 'b')
    logging.info(f"Part One: {value}")


# what is the value in register b after the program is finished executing if register a starts as 1 instead?
def part_two(instructions: list[str], args) -> None:
    register_values = defaultdict(int)
    register_values['a'] = 1
    value = run(instructions, register_values, 'b')
    logging.info(f"Part Two: {value}")


# `hlf r` sets register r to half its current value, then continues with the next instruction.
# `tpl r` sets register r to triple its current value, then continues with the next instruction.
# `inc r` increments register r, adding 1 to it, then continues with the next instruction.
# `jmp offset` is a jump; it continues with the instruction offset away relative to itself.
# `jie r, offset` is like jmp, but only jumps if register r is even ("jump if even").
# `jio r, offset` is like jmp, but only jumps if register r is 1 ("jump if one", not odd).

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
        input_data = [line.rstrip('\n') for line in input_file]
    if args.part == 1: part_one(input_data, args)
    elif args.part == 2: part_two(input_data, args)
