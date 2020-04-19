"""
Command line argument parsing
"""
import argparse
from typing import List


def parse_args(argv: List[str]):
    """
    :param argv: Command line arguments
    :return: Opened file (if '-f') or None, if it should use clipboard for input,
    and if it should use clipboard for output.
    """
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-c", "--copy",
                       help="Uses contents of a clipboard as input",
                       action="store_true", default=False)
    group.add_argument("-f", "--file", type=argparse.FileType('r'),
                       help="Uses contents of a text file as input",
                       default=None)
    parser.add_argument("-p", "--paste",
                        help="Pastes the link in a clipboard instead of printing",
                        action="store_true", default=False)
    parser.add_argument("-d", "--debug", help="Shows the log messages",
                        action="store_true", default=False)
    args = parser.parse_args(argv)
    return args


