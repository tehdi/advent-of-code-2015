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


def part_one(args) -> None:
    # target_r = 2978
    # target_c = 3083
    target_r = 2978
    target_c = 3083

    n = 20151125
    m = 252533
    d = 33554393

    r = 1
    c = 1
    max_r = 1
    max_c = 1

    while True:
        r -= 1
        c += 1
        if r < 1:
            max_r += 1
            r = max_r
            max_c += 1
            c = 1
        n = n * m % d
        # logging.debug(f"R{r} C{c} = {n}")
        if r == target_r and c == target_c:
            break

    logging.info(f"Part One: {n}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output-file', default=None)
    parser.add_argument('-v', '--verbose', default=False, action='store_true')
    args = parser.parse_args()
    configure_logging(args.verbose, args.output_file)

    part_one(args)
