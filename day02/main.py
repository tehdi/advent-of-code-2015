import logging
import argparse
import itertools

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
    total_paper = 0
    total_ribbon = 0
    with open(filename) as input_file:
        while (line := input_file.readline().rstrip()):
            dimensions = sorted(int(d) for d in line.split('x'))
            areas = []
            areas.append(dimensions[0] * dimensions[1])
            areas.append(2 * dimensions[0] * dimensions[1])
            areas.append(2 * dimensions[0] * dimensions[2])
            areas.append(2 * dimensions[1] * dimensions[2])
            paper_needed = sum(areas)
            perimeter = 2 * (dimensions[0] + dimensions[1])
            volume = dimensions[0] * dimensions[1] * dimensions[2]
            ribbon = perimeter + volume
            logging.debug(f"{dimensions}: Paper = {areas} => {paper_needed}, ribbon = {perimeter} + bow {volume} = {ribbon}")
            total_paper += paper_needed
            total_ribbon += ribbon
    logging.info(f"Paper: {total_paper}, Ribbon: {total_ribbon}")
