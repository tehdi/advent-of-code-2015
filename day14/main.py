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


def part_one(input_data: list[str], args) -> None:
    # I did this ON PAPER!
    logging.info(f"Part One: 2655")


def part_two(input_data: list[str], args) -> None:
    # I formatted my own input data instead of saving the AoC file
    # Mostly because my internet is down so I got it from my phone
    reindeers = [] # is totally the correct plural form
    for line in input_data[1:]:
        (name, speed, flight_time, rest_time) = line.split(',')
        reindeers.append({
            'name': name, 'speed': int(speed),
            'flight_time': int(flight_time), 'rest_time': int(rest_time),
            'cycle_time': int(flight_time) + int(rest_time),
            'distance': 0, 'points': 0 })
    for time in range(args.race_time):
        # at the end of each second,
        # all reindeers currently in the lead get one point each
        lead_distance = 0
        leaders = []
        for reindeer in reindeers:
            if time % reindeer['cycle_time'] < reindeer['flight_time']:
                reindeer['distance'] += reindeer['speed']
            if reindeer['distance'] == lead_distance:
                leaders.append(reindeer)
            elif reindeer['distance'] > lead_distance:
                lead_distance = reindeer['distance']
                leaders = [reindeer]
            # logging.debug(f"{time+1}s: {reindeer}")
        for leader in leaders: leader['points'] += 1
        # logging.debug(f"{time+1}s: LEADERS {lead_distance} = {leaders}")
    leader = None
    for reindeer in reindeers:
        if leader is None or reindeer['points'] > leader['points']: leader = reindeer
    # test expects:
    #   140s: Dancer 139, Comet 1, with Comet having just taken the lead this second
    #   1000s: Dancer 689 points at distance=1056, Comet 312 points at distance=1120
    # real answer: Vixen wins with 1059 points, at distance=2640
    # Congrats, Vixen!
    logging.info(f"Part Two: {leader}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input-file', default=None)
    parser.add_argument('-o', '--output-file', default=None)
    parser.add_argument('-v', '--verbose', default=False, action='store_true')
    parser.add_argument('-p', '--part', type=int, default=1)
    parser.add_argument('-t', '--race-time', type=int, default=2503)
    args = parser.parse_args()
    configure_logging(args.verbose, args.output_file)

    filename = args.input_file
    with open(filename) as input_file:
        input_data = [line.rstrip('\n') for line in input_file]
    if args.part == 1: part_one(input_data, args)
    elif args.part == 2: part_two(input_data, args)
