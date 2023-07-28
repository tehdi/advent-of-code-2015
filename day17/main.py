import logging
import argparse
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


class Container:
    def __init__(self, id, capacity):
        self.id = id
        self.capacity = capacity

    def key(self):
        return (self.id, self.capacity)

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return self.id


class Filler:
    def __init__(self, target, capacity, used_containers, available_containers):
        self.target = target
        self.capacity = capacity
        self.used_containers = [container for container in used_containers]
        self.available_containers = [container for container in available_containers]

    def key(self):
        return tuple([container.key() for container in sorted(self.used_containers, key=lambda c: c.id)])

    def __str__(self):
        return f"T{self.target} C{self.capacity} (U{[c.key() for c in self.used_containers]}) A{[c.key() for c in self.available_containers]}"


def part_one(input_data: list[str], args):
    containers = []
    for line_index,line in enumerate(input_data):
        containers.append(Container(line_index, int(line)))
    container_queue = deque(containers)
    filler_options = deque()
    while len(container_queue) > 0:
        container = container_queue.pop()
        ignore_index = containers.index(container)
        filler = Filler(args.target, container.capacity, [container], containers[:ignore_index] + containers[ignore_index+1:])
        filler_options.append(filler)
    ways_found = 0
    fillers_filled = []
    ways_used = set()
    while len(filler_options) > 0:
        filler = filler_options.pop()
        if filler.key() in ways_used: continue
        ways_used.add(filler.key())
        if filler.capacity > filler.target: continue
        if filler.capacity == filler.target:
            ways_found += 1
            fillers_filled.append(filler)
            continue
        for i in range(len(filler.available_containers)):
            container = filler.available_containers[i]
            new_filler = Filler(args.target,
                filler.capacity + container.capacity,
                filler.used_containers + [container],
                filler.available_containers[:i] + filler.available_containers[i+1:]
            )
            filler_options.append(new_filler)
    # test: 25 litres => 4 ways
    # actual: 150 litres => ? ways
    logging.info(f"Part One: {ways_found}")
    logging.debug(f"{[str(filler) for filler in fillers_filled]}")
    return fillers_filled


# find the minimum number of containers to fit exactly 150L
# and then find how many combinations use that many
def part_two(input_data: list[str], args) -> None:
    fillers_filled = part_one(input_data, args)
    min_containers = min([len(filler.used_containers) for filler in fillers_filled])
    matching_containers = [filler for filler in fillers_filled if len(filler.used_containers) == min_containers]
    logging.info(f"Part Two: {len(matching_containers)} ways to use {min_containers} containers to get {args.target} litres")
    logging.debug(f"{[str(filler) for filler in matching_containers]}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input-file', default=None)
    parser.add_argument('-o', '--output-file', default=None)
    parser.add_argument('-v', '--verbose', default=False, action='store_true')
    parser.add_argument('-p', '--part', type=int, default=1)
    parser.add_argument('-t', '--target', type=int, default=150)
    args = parser.parse_args()
    configure_logging(args.verbose, args.output_file)

    filename = args.input_file
    with open(filename) as input_file:
        input_data = [line.rstrip('\n') for line in input_file]
    if args.part == 1: part_one(input_data, args)
    elif args.part == 2: part_two(input_data, args)
