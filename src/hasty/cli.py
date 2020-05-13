"""
Command line argument parsing
"""
from argparse import ArgumentParser, Namespace, ArgumentTypeError
from pathlib import Path
from typing import List, Optional


def readable_file(path: str) -> Path:
    file = Path(path).resolve()
    if file.is_file():
        return file
    else:
        raise ArgumentTypeError(f"readable_dir:{path} is not a valid path")


def parse_args(cli_args: Optional[List[str]] = None) -> Namespace:
    """
    :param cli_args: List of arguments. If nothing is passed, uses sys.argv
    :return: Opened file (if '-f') or None, if it should use clipboard for input,
    if it should use clipboard for output, and if should show debug messages in log.
    """
    parser = ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-c", "--copy",
                       help="Uses contents of a clipboard as input",
                       action="store_true", default=False)
    group.add_argument("-f", "--file", type=readable_file,
                       help="Path to a text file used as input",
                       default=None)
    parser.add_argument("-p", "--paste",
                        help="Pastes the link in a clipboard instead of printing",
                        action="store_true", default=False)
    parser.add_argument("-d", "--debug", help="Shows the log messages",
                        action="store_true", default=False)
    # if None is passed, it uses sys.argv
    args = parser.parse_args(cli_args)
    return args


