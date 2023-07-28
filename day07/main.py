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


class Operation:
    def __init__(self, input_wires: list[str], output_wire: str, operation: Callable) -> None:
        self.input_wires = input_wires
        self.output_wire = output_wire
        self.operation = operation

    def is_ready(self, wires: dict[str, int]) -> bool:
        return all([(wire.isdigit() or wire in wires) for wire in self.input_wires])

    def operate(self, inputs) -> int:
        return self.operation(inputs)

    def __str__(self) -> str:
        return f"[{self.operation}] applied to [{self.input_wires}] outputs to [{self.output_wire}]"


def is_value_input(inputs: list[str]) -> bool:
    return len(inputs) == 1 and inputs[0].isdigit()

def operation_value(values: list[int]) -> int:
    value = values[0]
    logging.debug(f"VALUE: {value}")
    return value

def operation_not(values: list[int]) -> int:
    # I could format the input to 16 bits, then NOT the whole thing: '{0:016b}'.format(value)
    # or I can subtract the input from 2^16-1 and get the same answer
    value = MAX_VALUE - values[0]
    logging.debug(f"NOT {values[0]}: {value}")
    return value

def operation_lshift(bitcount: int) -> int:
    def apply(values: list[int]) -> int:
        value = values[0] << bitcount
        logging.debug(f"{values[0]} LSHIFT {bitcount}: {value}")
        return value
    return apply

def operation_rshift(bitcount: int) -> int:
    def apply(values: list[int]) -> int:
        value = values[0] >> bitcount
        logging.debug(f"{values[0]} RSHIFT {bitcount}: {value}")
        return value
    return apply

def operation_or(values: list[int]) -> int:
    value = values[0] | values[1]
    logging.debug(f"{values[0]} OR {values[1]}: {value}")
    return value

def operation_and(values: list[int]) -> int:
    value = values[0] & values[1]
    logging.debug(f"{values[0]} AND {values[1]}: {value}")
    return value

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


def part_one(input_data: list[str], args) -> dict[str, int]:
    wires = {} # name:str = value:int
    operations = deque()
    line_pattern = re.compile('(.+) -> (.+)$')
    for line in input_data:
        m = line_pattern.match(line)
        inputs = m.group(1).split()
        output_wire = m.group(2)
        if is_value_input(inputs):
            wires[output_wire] = int(inputs[0])
            logging.debug(f"{output_wire} = {wires[output_wire]}")
        else:
            (operation, input_wires) = parse_inputs(inputs)
            operations.append(Operation(input_wires, output_wire, operation))
    while len(operations) > 0:
        operation = operations.popleft()
        if not operation.is_ready(wires):
            # to the back of the queue
            operations.append(operation)
            continue
        inputs = [int(wire) if wire.isdigit() else wires[wire] for wire in operation.input_wires]
        # some might exceed max value, so truncate them to just the 16 bits we can use
        value = operation.operate(inputs) & MAX_VALUE
        wires[operation.output_wire] = value
        logging.debug(f"{operation} = {value}")
    logging.debug(wires)
    logging.info(f"Part One: {wires.get('a')}")
    return wires


# take the value that part one gave for wire a
# and feed it into wire b
# then run everything again and see what the new output on wire a is
# easiest way is to make a second input file with just the value going into b changed, right?
def part_two(input_data: list[str], args) -> None:
    wires = part_one(input_data, args)
    logging.info(f"Part Two: {wires.get('a')}")


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
