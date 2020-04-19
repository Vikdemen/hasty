import pytest
from hasty import cli


def test_args_none():
    """
    Without args program should use stdin and print to stdout
    """
    args = cli.parse_args([])
    assert not args.copy
    assert not args.paste
    assert args.file is None
    assert not args.debug


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
    args = cli.parse_args(['-c'])
    assert args.copy
    args = cli.parse_args(['--copy'])
    assert args.copy


def test_args_paste():
    """
    Uses clipboard for output when called with "--paste"
    """
    args = cli.parse_args(['-p'])
    assert args.paste
    args = cli.parse_args(['--paste'])
    assert args.paste


def test_args_file():
    """
    With filename and "--file" argument, argparse tries to open the file
    """
    with pytest.raises(SystemExit):
        cli.parse_args(['-f', 'invalidfilename'])
    # TODO - mock file opening


def test_args_debug():
    """
    With "--debug" argument, logging level is set to "Debug"
    """
    args = cli.parse_args(['-d'])
    assert args.debug
    args = cli.parse_args(['--debug'])
    assert args.debug


def test_args_combination():
    """
    Arguments can be combined
    """
    args = cli.parse_args(['-cp'])
    assert args.copy
    assert args.paste
    args = cli.parse_args(['-c', '-p'])
    assert args.copy
    assert args.paste


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
