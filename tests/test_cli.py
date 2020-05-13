import pytest
from hasty import cli


def test_args_none():
    """
    Without args program should use stdin and print to stdout, and debug is off
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


def test_args_valid_file(fake_file):
    """
    With filename and "--file" argument, argparse tries to open the file
    """
    args = cli.parse_args(['-f', str(fake_file.path)])
    assert args.file == fake_file.path


def test_args_invalid_file():
    """
    Gives error when filename is not valid
    """
    with pytest.raises(SystemExit):
        cli.parse_args(['-f', 'invalidfilename'])


def test_filename_required():
    """
    You can't use file parameter without specifying the filename
    """
    with pytest.raises(SystemExit):
        cli.parse_args(['-f'])


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
