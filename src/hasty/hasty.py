"""
Python alternative for haste-client CLI utility
"""
import io
import logging
import sys
from typing import List, Optional

import pyperclip
import requests
from hasty import cli, config

URL = str


def main(argv: List[str]) -> None:
    """
    :param argv: A list of console arguments
    :return: None
    """
    args = cli.parse_args(argv)

    logger = set_logger(args.debug)
    settings = config.Config(logger=logger)

    url = settings.url

    text = get_text(args.copy, args.file)
    hastebin = Hastebin(url, logger)
    try:
        text_link = hastebin.paste(text)
        show_link(text_link, args.paste)
    except requests.RequestException:
        print('Service is unavailable')


def set_logger(debug: bool = False):
    logger = logging.getLogger(__name__)
    level = logging.DEBUG if debug else logging.WARNING
    logging.basicConfig(level=level)
    return logger


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


class Hastebin:
    """
    Interface with hastebin-based site
    """

    def __init__(self, url: URL, logger=None):
        """
        :param url: Url in https://hastebin.com/ format
        """
        self.url = url
        self.logger = logger

    def paste(self, text: str) -> URL:
        """
        Sends the text to hastebin-based site
        :param text: Text to post on hastebin
        :return: Link to the paste`
        """
        if self.logger is not None:
            self.logger.debug(f'Text received is {text}')
            self.logger.debug(f'Pasting to {self.url}')
        response = requests.post(self.url + 'documents', text)
        if self.logger is not None:
            self.logger.debug(f'Response code is {response.status_code}')
        if response.ok:
            key: str = response.json()['key']
            if self.logger is not None:
                self.logger.info(f'Link received is {self.url}{key}')
            return self.url + key
        else:
            self.logger.error(f'Invalid response code {response.status_code}')
            raise requests.RequestException()
