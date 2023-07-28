import logging
import argparse
import re
from typing import Callable
from collections import deque

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


MAX_VALUE = 2**16 - 1


def operation_value(values: list[int]) -> int:
    value = values[0]
    return value

def operation_not(values: list[int]) -> int:
    # I could format the input to 16 bits, then NOT the whole thing: '{0:016b}'.format(value)
    # or I can subtract the input from 2^16-1 and get the same answer
    return MAX_VALUE - values[0]

def operation_lshift(bitcount: int) -> int:
    def apply(values: list[int]) -> int:
        return values[0] << bitcount
    return apply

def operation_rshift(bitcount: int) -> int:
    def apply(values: list[int]) -> int:
        return values[0] >> bitcount
    return apply

def operation_or(values: list[int]) -> int:
    return values[0] | values[1]

def operation_and(values: list[int]) -> int:
    return values[0] & values[1]

def parse_inputs(inputs: list[str]) -> tuple[Callable, list[str]]:
    # {wire} (a value input but without a literal value being input)
    if len(inputs) == 1:
        return (operation_value, [inputs[0]])
    # NOT {wire}
    if len(inputs) == 2:
        return (operation_not, [inputs[1]])
    # {wire} LSHIFT {bitcount}
    if 'LSHIFT' in inputs[1]:
        return (operation_lshift(int(inputs[2])), [inputs[0]])
    # {wire} RSHIFT {bitcount}
    if 'RSHIFT' in inputs[1]:
        return (operation_rshift(int(inputs[2])), [inputs[0]])
    # {wire} OR {wire}
    if 'OR' in inputs[1]:
        return (operation_or, [inputs[0], inputs[2]])
    # {wire} AND {wire}
    return (operation_and, [inputs[0], inputs[2]])

def calculate(wires: dict[str, str], wire_name: str) -> int:
    if wire_name.isdigit():
        return int(wire_name)
    if type(value := wires[wire_name]) is int:
        return value
    inputs = wires[wire_name].split(' ')
    (operation, input_wires) = parse_inputs(inputs)
    for name in input_wires:
        value = calculate(wires, name)
        wires[name] = value
        logging.debug(f"{wire_name} = {value}")
    return operation([wires[name] for name in input_wires])


def part_one(input_data: list[str], args) -> int:
    line_pattern = re.compile('(.+) -> (.+)$')
    wires = {}
    for line in input_data:
        m = line_pattern.match(line)
        inputs = m.group(1)
        output_wire = m.group(2)
        wires[output_wire] = inputs
    value = calculate(wires, 'a')
    logging.info(f"Part One: {value}")
    return value


def part_two(input_data: list[str], args) -> None:
    line_pattern = re.compile('(.+) -> (.+)$')
    wires = {}
    for line in input_data:
        m = line_pattern.match(line)
        inputs = m.group(1)
        output_wire = m.group(2)
        wires[output_wire] = inputs
    wires['b'] = part_one(input_data, args)
    value = calculate(wires, 'a')
    logging.info(f"Part Two: {value}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input-file', default=None)
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
