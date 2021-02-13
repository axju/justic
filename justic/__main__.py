import argparse
import logging

from justic import Justic, __version__


def set_logger(verbose):
    levels = [logging.WARNING, logging.INFO, logging.DEBUG]
    level = levels[min(len(levels) - 1, verbose)]
    logging.basicConfig(level=level,
                        format="%(asctime)s %(levelname)s %(message)s")


def main(argv=None):
    parser = argparse.ArgumentParser(prog='justic')
    parser.add_argument('-V', '--version', action='version', version=__version__)
    parser.add_argument('-v', '--verbose', action='count', default=0)
    parser.add_argument('-d', '--delete', action='store_true')
    parser.add_argument('-c', '--config', default='justiconf.py')
    parser.add_argument('workdir', nargs='?', default='.')

    args = parser.parse_args(argv)
    set_logger(args.verbose)
    justic = Justic(root=args.workdir, target=args.config)
    justic.run()


if __name__ == '__main__':
    main()
