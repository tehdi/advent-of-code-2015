import logging
import argparse
import re
from collections import defaultdict, deque
from random import randint
from queue import PriorityQueue

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


class MoleculeTracker:
    def __init__(self, molecule, steps):
        self.molecule = molecule
        self.steps = steps

    def __lt__(self, other):
        return len(self.molecule) < len(other.molecule)


def parse_input(data):
    replacements = defaultdict(list)
    original_molecule = ''
    done_replacements = False
    for line in data:
        if done_replacements:
            original_molecule = line
            break
        if line == '':
            done_replacements = True
            continue
        splits = line.split(' => ')
        replacements[splits[0]].append(splits[1])
    return (original_molecule, replacements)

def part_one(input_data: list[str], args) -> None:
    (original_molecule, replacements) = parse_input(input_data)
    replacement_molecules = set()
    element = ''
    for i in range(len(original_molecule)):
        if original_molecule[i].isupper(): element = ''
        element += original_molecule[i]
        if element not in replacements: continue
        head_stop_index = i - len(element) + 1
        tail_start_index = head_stop_index + len(element)
        head = original_molecule[:head_stop_index]
        tail = original_molecule[tail_start_index:]
        for r in replacements[element]:
            replacement_molecules.add(head + r + tail)
        element = ''
    logging.info(f"Part One: {len(replacement_molecules)}")

def dead_end(molecule_tracker, fastest_seen):
    molecule = molecule_tracker.molecule
    steps = molecule_tracker.steps
    if steps > fastest_seen.get('e', steps):
        logging.debug(f"D: e ({fastest_seen['e']}): S{steps} M{len(molecule)}")
        return True
    if steps >= fastest_seen.get(molecule, steps+1):
        logging.debug(f"D: m ({fastest_seen[molecule]}): S{steps} M{len(molecule)}")
        return True
    if 'e' in molecule and len(molecule) > 1:
        logging.debug(f"D: es: S{steps} M{len(molecule)}")
        return True
    return False

def part_two(input_data: list[str], args) -> None:
    (target_molecule, replacements) = parse_input(input_data)
    backwards = { v:k for k,vs in replacements.items() for v in vs}
    paths = PriorityQueue()
    paths.put((len(target_molecule), MoleculeTracker(target_molecule, 0)))
    fastest_seen = {}
    while not paths.empty():
        molecule_tracker = paths.get()[1]
        if dead_end(molecule_tracker, fastest_seen): continue
        molecule = molecule_tracker.molecule
        steps = molecule_tracker.steps
        if args.logging_frequency > 0 and randint(1, args.logging_frequency) == args.logging_frequency:
            logging.debug(f"P{paths.qsize()}: S{steps}: M{len(molecule)} => {molecule}")
        fastest_seen[molecule] = steps
        if molecule == 'e':
            logging.info(f"New fastest e! {steps}")
            break
        for element in backwards:
            if not element in molecule: continue
            new_molecules = [molecule[:s] + backwards[element] + molecule[s+len(element):] for s in
                [m.start() for m in re.finditer(f"(?={element})", molecule)]]
            for new_molecule in new_molecules:
                paths.put((len(new_molecule), MoleculeTracker(new_molecule, steps+1)))
    logging.info(f"Part Two: {fastest_seen.get('e', 0)}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input-file', default=None)
    parser.add_argument('-o', '--output-file', default=None)
    parser.add_argument('-v', '--verbose', default=False, action='store_true')
    parser.add_argument('-p', '--part', type=int, default=1)
    parser.add_argument('-l', '--logging-frequency', type=int, default=1000)
    args = parser.parse_args()
    configure_logging(args.verbose, args.output_file)

    filename = args.input_file
    with open(filename) as input_file:
        input_data = [line.rstrip('\n') for line in input_file]
    if args.part == 1: part_one(input_data, args)
    elif args.part == 2: part_two(input_data, args)
