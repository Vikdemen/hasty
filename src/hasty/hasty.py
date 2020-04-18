"""
Python alternative for haste-client CLI utility
"""
import io
import sys
from typing import List, Optional

import pyperclip
import requests
from hasty import cli, config

URL = str


class Hastebin:
    """
    Interface with hastebin-based site
    """

    def __init__(self, url: URL):
        """
        :param url: Url in https://hastebin.com/ format
        """
        # TODO - validation
        self.url = url

    def paste(self, text: str) -> URL:
        """
        Sends the text to hastebin-based site
        :param text: Text to post on hastebin
        :return: Link to the paste`
        """
        response = requests.post(self.url + 'documents', text)
        if response:
            key: str = response.json()['key']
            return self.url + key
        else:
            raise requests.RequestException()


def main(argv: List[str]) -> None:
    """
    :param argv: A list of console arguments
    :return: None
    """
    source, from_clipboard, to_clipboard = cli.parse_args(argv)
    url = config.HASTEBIN_URL
    text = get_text(from_clipboard, source)
    hastebin = Hastebin(url)
    try:
        text_link = hastebin.paste(text)
        show_link(text_link, to_clipboard)
    except requests.RequestException:
        print('Service is unavailable')


def get_text(clipboard: bool, source: Optional[io.TextIOWrapper]) -> str:
    """
    :param clipboard: If it should use clipboard as input
    :param source: If it doesn't use clipboard, it uses either file contents or stdin
    :return:
    """
    if clipboard:
        text = pyperclip.paste()
    else:
        if source is None:
            source = sys.stdin
        try:
            text = source.read()
        finally:
            source.close()
    return text


def show_link(text_link: URL, clipboard: bool) -> None:
    """
    :param text_link: URL to print
    :param clipboard: Whether you should use clipboard or stdout
    :return:
    """
    if clipboard:
        pyperclip.copy(text_link)
    else:
        print(text_link)
