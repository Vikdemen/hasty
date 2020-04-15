from src.hasty import hasty, cli
import pytest
import requests_mock


def test_bin():
    url = 'https://helloworld.com/'
    webbin = hasty.Hastebin(url)
    assert webbin.url == url


def test_paste():
    with requests_mock.Mocker() as mock_api:
        url = 'https://helloworld.com/'
        mock_response = 'hello111'
        mock_link = url + mock_response
        mock_api.post(url + 'documents', json={'key': mock_response})

        hastebin = hasty.Hastebin(url)
        link = hastebin.paste('hello world')
        assert link == mock_link


# TODO - test error handling

def test_args_none():
    args = hasty.parse_args([])
    assert not args.paste
    assert not args.copy
    assert args.file is None


def test_args_help():
    with pytest.raises(SystemExit):
        cli.parse_args(['-h'])


def test_args_copy():
    args = cli.parse_args(['-c'])
    assert args.copy
    args = cli.parse_args([])
    assert not args.copy


def test_args_paste():
    args = cli.parse_args(['-p'])
    assert args.paste
    args = cli.parse_args([])
    assert not args.paste


def test_args_combination():
    args = cli.parse_args(['-cp'])
    assert args.copy
    assert args.paste
    args = cli.parse_args(['-c', '-p'])
    assert args.copy
    assert args.paste


def test_exclusive_args():
    with pytest.raises(SystemExit):
        cli.parse_args(['-c', '-f', 'filename'])
    with pytest.raises(SystemExit):
        cli.parse_args(['-cf'])


def test_file_required():
    with pytest.raises(SystemExit):
        cli.parse_args(['-f'])