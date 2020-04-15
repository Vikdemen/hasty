import argparse
import functools
import sys
import io
from typing import List, Callable, Tuple, Optional

import pyperclip


def get_io() -> Tuple[Callable[[], str], Callable[[str], None]]:
    args = parse_args(sys.argv[1:])
    input_method = choose_input(args)
    output_method = choose_output(args)
    return input_method, output_method


def parse_args(args: List[str]) -> argparse.Namespace:
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
    args = parser.parse_args(args)
    return args


def choose_input(args) -> Callable[[], str]:
    if args.copy:
        input_method = pyperclip.paste
    else:
        input_method = functools.partial(get_input, args.file)
    return input_method


def choose_output(args) -> Callable[[str], None]:
    if args.paste:
        output_method = pyperclip.copy
    else:
        output_method = print
    return output_method


def get_input(source: Optional[io.TextIOWrapper]) -> str:
    if source is None:
        source = sys.stdin
    with source:
        text = source.read()
    return text
