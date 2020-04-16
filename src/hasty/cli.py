import argparse
import functools
import sys
import io
from typing import List, Callable, Tuple

import pyperclip


def get_io(params: List[str]) -> Tuple[Callable[[], str], Callable[[str], None]]:
    """
    :param params: command line parameters
    :return: Function for data input and function for data output
    """
    file, copy, paste = parse_args(params)
    input_method = choose_input(file, copy)
    output_method = choose_output(paste)
    return input_method, output_method


def parse_args(args: List[str]) -> Tuple[io.TextIOWrapper, bool, bool]:
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
    copy = args.copy
    paste = args.paste
    file = args.file
    if file is None:
        file = sys.stdin
    return file, copy, paste


def choose_input(file: io.TextIOWrapper, copy: bool) -> Callable[[], str]:
    if copy:
        input_method = pyperclip.paste
    else:
        input_method = functools.partial(get_input, file)
    return input_method


def choose_output(paste: bool) -> Callable[[str], None]:
    if paste:
        output_method = pyperclip.copy
    else:
        output_method = print
    return output_method


def get_input(source: io.TextIOWrapper) -> str:
    """
    :param source: File wrapper to read data from. Uses stdin if None.
    :return: Function that reads data from given IO
    """
    with source:
        text = source.read()
    return text
