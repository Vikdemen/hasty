"""
Command line argument parsing
"""
import argparse
import io
from typing import List, Tuple, Optional


def parse_args(argv: List[str]) -> Tuple[Optional[io.TextIOWrapper], bool, bool]:
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
    args = parser.parse_args(argv)
    from_clipboard = args.copy
    to_clipboard = args.paste
    file = args.file
    return file, from_clipboard, to_clipboard


