import pytest
from hasty import cli


def test_args_none():
    """
    Without args program should use stdin and print to stdout
    """
    file, from_clipboard, to_clipboard = cli.parse_args([])
    assert not to_clipboard
    assert not from_clipboard
    assert file is None


def test_args_help():
    """
    Shows help without running the program
    """
    with pytest.raises(SystemExit):
        cli.parse_args(['-h'])
    with pytest.raises(SystemExit):
        cli.parse_args(['--help'])


def test_args_copy():
    """
    Uses clipboard for input when called with "--copy"
    """
    file, from_clipboard, paste = cli.parse_args(['-c'])
    assert from_clipboard
    file, from_clipboard, paste = cli.parse_args(['--copy'])
    assert from_clipboard


def test_args_paste():
    """
    Uses clipboard for output when called with "--paste"
    """
    file, from_clipboard, to_clipboard = cli.parse_args(['-p'])
    assert to_clipboard
    file, from_clipboard, to_clipboard = cli.parse_args(['--paste'])
    assert to_clipboard


def test_args_file():
    """
    With filename and "--file" argument, argparse tries to open the file
    """
    with pytest.raises(SystemExit):
        cli.parse_args(['-f', 'invalidfilename'])
    # TODO - mock file opening


def test_args_combination():
    """
    Arguments can be combined
    """
    file, copy, paste = cli.parse_args(['-cp'])
    assert copy
    assert paste
    file, copy, paste = cli.parse_args(['-c', '-p'])
    assert copy
    assert paste


def test_exclusive_args():
    """
    You can't use both clipboard and file as input
    """
    with pytest.raises(SystemExit):
        cli.parse_args(['-cf', 'filename'])
    with pytest.raises(SystemExit):
        cli.parse_args(['-cf'])


def test_filename_required():
    """
    :return: You can't use file parameter without specifying the filename
    """
    with pytest.raises(SystemExit):
        cli.parse_args(['-f'])
