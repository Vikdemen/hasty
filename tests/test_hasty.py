"""
Unit testing
"""
import sys
from typing import Callable, NamedTuple
from unittest.mock import Mock
import pytest

import pyperclip
import requests
import responses
from hasty import hasty


class Paste(NamedTuple):
    """
    Container for mock values
    """
    url: str
    key: str
    text: str

    @property
    def link(self):
        """
        Creates full fake url from parts
        """
        return self.url + self.key


@pytest.fixture
def fake_paste():
    """
    Mock values
    """
    paste = Paste(url='https://helloworld.com/', key='hello111', text='Hello world!')
    return paste


@pytest.fixture
def testing_app(fake_paste):
    """
    Creates instance that takes in mock data
    """
    get_text = Mock(return_value=fake_paste.text)
    show_link = Mock()
    app = hasty.Hasty(url=fake_paste.url, text_source=get_text, link_output=show_link)
    return app


def test_app_creation():
    """
    Class should be created without errors
    """
    url = 'fakeurl'
    text_source = Mock()
    link_output = Mock()
    app = hasty.Hasty(url, text_source, link_output)
    assert app.url == url
    assert app.get_text == text_source
    assert app.show_link == link_output


def test_hasty_run(testing_app, fake_paste):
    """
    App should get text and try to output link
    """
    testing_app.paste = Mock(return_value=fake_paste.link)
    testing_app.run()
    # noinspection PyUnresolvedReferences
    assert testing_app.get_text.called
    # noinspection PyUnresolvedReferences
    testing_app.show_link.assert_called_with(fake_paste.link)


def test_get_text_assigns_stdin():
    """
    Reads from stdin
    """
    get_text = hasty.get_text_source(source=None, clipboard=False)
    assert get_text == sys.stdin.read


def test_get_text_uses_clipboard():
    """
    Uses text from clipboard
    """
    get_text = hasty.get_text_source(clipboard=True, source=None)
    assert get_text == pyperclip.paste


def test_get_text_reads_from_file(fake_file):
    """
    Uses file contents
    """
    get_text = hasty.get_text_source(clipboard=False, source=fake_file.path)
    assert get_text == fake_file.path.read_text


@pytest.mark.parametrize("expected_func, clipboard", [
    (pyperclip.copy, True),
    (print, False),
])
def test_show_link(expected_func: Callable[[str], None], clipboard: bool):
    """
    When clipboard is True, link is printed to clipboard, when False, link is printed to stdout
    """
    show_link = hasty.get_link_output(clipboard=clipboard)
    assert show_link == expected_func


@pytest.mark.parametrize("error_type", [requests.ConnectionError, requests.HTTPError])
def test_run_handles_errors(testing_app, error_type):
    """
    Handles errors by catching them and logging to stderr
    """
    testing_app.paste = Mock(side_effect=error_type)
    testing_app.run()
    # noinspection PyUnresolvedReferences
    assert testing_app.paste.called
    # noinspection PyUnresolvedReferences
    assert not testing_app.show_link.called


@responses.activate
def test_paste_raises_connection_error(testing_app, fake_paste):
    with pytest.raises(requests.ConnectionError):
        testing_app.paste(fake_paste.text)


@responses.activate
def test_paste_makes_post_request(testing_app, fake_paste):
    responses.add(responses.POST, fake_paste.url + 'documents',
                  json={'key': fake_paste.key}, status=200)
    link = testing_app.paste(fake_paste.text)
    assert link == fake_paste.link


@responses.activate
def test_paste_bad_request(testing_app, fake_paste):
    responses.add(responses.POST, fake_paste.url + 'documents',
                  json={'error': 'not found'}, status=404)
    with pytest.raises(requests.HTTPError):
        testing_app.paste(fake_paste.text)


@responses.activate
def test_paste_invalid_response(testing_app, fake_paste):
    responses.add(responses.POST, fake_paste.url + 'documents',
                  json={'invalidkey': 'invalid'}, status=200)
    with pytest.raises(KeyError):
        testing_app.paste(fake_paste.text)
