import sys

import pyperclip
import pytest
from hasty import cli


def test_choose_io_copy():
    input_method, output_method = cli.get_io(['-c'])
    assert input_method == pyperclip.paste


def test_choose_io_paste():
    input_method, output_method = cli.get_io(['-p'])
    assert output_method == pyperclip.copy

# TODO - ambigious parameters


def test_args_none():
    file, copy, paste = cli.parse_args([])
    assert not paste
    assert not copy
    assert file is sys.stdin


def test_args_help():
    with pytest.raises(SystemExit):
        cli.parse_args(['-h'])


def test_args_copy():
    file, copy, paste = cli.parse_args(['-c'])
    assert copy


def test_args_paste():
    file, copy, paste = cli.parse_args(['-p'])
    assert paste


def test_args_combination():
    file, copy, paste = cli.parse_args(['-cp'])
    assert copy
    assert paste
    file, copy, paste = cli.parse_args(['-c', '-p'])
    assert copy
    assert paste


def test_exclusive_args():
    with pytest.raises(SystemExit):
        cli.parse_args(['-c', '-f', 'filename'])
    with pytest.raises(SystemExit):
        cli.parse_args(['-cf'])


def test_file_required():
    with pytest.raises(SystemExit):
        cli.parse_args(['-f'])

