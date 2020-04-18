import io
import unittest.mock as mock

import requests_mock
from hasty import hasty


def test_main(monkeypatch):
    """
    Reads the input, pastes the text to hastebin, then prints the link
    """
    url = 'https://hastebin.com/'
    mock_response = 'hello111'
    mock_link = url + mock_response
    result = ''

    def mock_input(*args, **kwargs):
        return 'hello world'

    def mock_output(link, *args, **kwargs):
        nonlocal result
        result = link

    def hastebin_mock(*args, **kwargs):
        return mock_link

    monkeypatch.setattr('hasty.hasty.get_text', mock_input)
    monkeypatch.setattr('hasty.hasty.show_link', mock_output)
    monkeypatch.setattr('hasty.hasty.Hastebin.paste', hastebin_mock)
    hasty.main([])
    assert result == mock_link


def test_bin():
    """
    Checks proper class creation
    """
    url = 'https://helloworld.com/'
    hastebin = hasty.Hastebin(url)
    assert hastebin.url == url


def test_paste():
    with requests_mock.Mocker() as mock_api:
        url = 'https://helloworld.com/'
        mock_response = 'hello111'
        mock_link = url + mock_response
        mock_api.post(url + 'documents', json={'key': mock_response})

        hastebin = hasty.Hastebin(url)
        link = hastebin.paste('hello world')
        assert link == mock_link


# def test_paste_error():
#     with requests_mock.Mocker() as mock_api:
#         url = 'https://hastebin.com/'
#         mock_response = 'hello111'
#         mock_api.post(url + 'documents', json={'key': mock_response})
#
#         hastebin = hasty.Hastebin('https://helloworld.com/')
#         with pytest.raises(requests.RequestException):
#             hastebin.paste('hello world')
# TODO - get the mocker to return failed requests


def test_get_text_from_io():
    text = 'Hello world'
    source = io.StringIO(text)
    result = hasty.get_text(source=source, clipboard=False)
    assert result == text


def text_get_from_stdin(monkeypatch):
    text = 'Hello world'
    monkeypatch.setattr('sys.stdin', io.StringIO(text))
    result = hasty.get_text(source=None, clipboard=False)
    assert result == text


def test_get_text_from_clipboard(monkeypatch):
    text = 'Hello world'
    mock_func = mock.Mock()
    mock_func.return_value = text
    monkeypatch.setattr('pyperclip.paste', mock_func)
    result = hasty.get_text(clipboard=True, source=None)
    assert result == text


def test_show_link_to_clipboard(monkeypatch):
    link = 'https://helloworld.com/hello111'
    result = ''

    def mock_clip(text):
        nonlocal result
        result = text

    monkeypatch.setattr('pyperclip.copy', mock_clip)
    hasty.show_link(link, clipboard=True)
    assert result == link


def test_show_link_to_stdout(capsys):
    link = 'https://helloworld.com/hello111'
    hasty.show_link(link, clipboard=False)
    result = capsys.readouterr().out.rstrip('\n')
    assert result == link
