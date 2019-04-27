#!/usr/bin/env python

"""example is an example Python library and tool

Usage:
  example [--log-level=LEVEL]
  example (-h | --help)

Options:
  -h --help              Show this message.
  --log-level=LEVEL      If specified, then the log level will be set to
                         the specified value.  Valid values are "debug", "info",
                         "warning", "error", and "critical". [default: warning]
"""

import logging
import sys

import docopt
import ipaddress

from .lcgit import RandomNetworkSequence


def example():
    """A dummy function."""
    net = ipaddress.ip_network("64.69.57.0/24")

    rns = RandomNetworkSequence(net)
    for i in rns:
        print(i)


def main():
    args = docopt.docopt(__doc__, version="0.0.1")

    # Set up logging
    log_level = args["--log-level"]
    try:
        logging.basicConfig(
            format="%(asctime)-15s %(levelname)s %(message)s", level=log_level.upper()
        )
    except ValueError:
        logging.critical(
            f'"{log_level}" is not a valid logging level.  Possible values '
            "are debug, info, warning, and error."
        )
        return 1

    example()

    # Stop logging and clean up
    logging.shutdown()


if __name__ == "__main__":
    sys.exit(main())
