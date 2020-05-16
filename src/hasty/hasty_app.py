"""
Python alternative for haste-client CLI program.
"""
import logging

import sys
from pathlib import Path
from typing import Callable, Optional

import pyperclip
import requests

URL = str


def get_text_source(clipboard: bool, source: Optional[Path]) -> Callable[[], str]:
    """
    :param clipboard: If it should use clipboard or stdin/file
    :param source: File to get text from, uses stdin if none
    :return: Function that is used to grab the text
    """
    logger = logging.getLogger(__name__)

    if clipboard:
        assert source is None
        logger.debug('Text will be loaded from clipboard')
        return pyperclip.paste
    else:
        if source is None:
            logger.debug('Text will be loaded from  command line')
            return sys.stdin.read
        else:
            assert source.is_file()
            logger.debug(f'Text will be loaded from {source}')
            return source.read_text


def get_link_output(clipboard: bool) -> Callable[[URL], None]:
    """
    :param clipboard: If it should use clipboard
    :return: Function that is used to output the link
    """
    logger = logging.getLogger(__name__)

    if clipboard:
        logger.debug('Link will be printed in clipboard')
        return pyperclip.copy
    else:
        logger.debug('Link will be printed in command line')
        # noinspection PyTypeChecker
        # apparently the signature of print is too complex
        return print


class HasteClient:
    """
    Class that allows to paste text on hastebin-based websites and retrieve the link
    """
    def __init__(self, url: URL, text_source: Callable[[], str], link_output: Callable[[str], None]):
        """
        :param url: Url in https://hastebin.com/ format
        :param text_source: Function which is used to get the input
        :param link_output: Function which is used to output the result
        """
        self.url = url
        self.get_text = text_source
        self.show_link = link_output
        self.logger = logging.getLogger(__name__)

    def run(self) -> None:
        """
        Gets the text, posts it on a website and shows the link
        """
        text = self.get_text()
        try:
            link = self.paste(text)
        except (KeyError, ValueError) as ex:
            logging.debug(ex, exc_info=True)
            logging.error('Invalid response format')
        except requests.exceptions.ConnectionError as ex:
            logging.debug(ex, exc_info=True)
            logging.error('Unable to establish internet connection')
        except requests.exceptions.HTTPError as ex:
            logging.debug(ex, exc_info=True)
            logging.error('Service is unavailable')
        except requests.exceptions.RequestException as ex:
            logging.debug(ex, exc_info=True)
            logging.error('Unknown error while making a request')
        else:
            logging.info('Task successful')
            self.show_link(link)

    def paste(self, text: str) -> URL:
        """
        Sends the text to hastebin-based site
        :param text: Text to post on hastebin
        :return: Link to the pasted text.
        :raises KeyError: Invalid JSON
        :raises ValueError: No JSON in response
        :raises ConnectionError: No internet connection
        :raises HTTPError: Bad response
        """
        self.logger.debug(f'Text received is {text}')
        self.logger.debug(f'Pasting to {self.url}')
        response = requests.post(self.url + 'documents', text)
        if response.ok:
            self.logger.debug(f'Response code is {response.status_code}')
        else:
            self.logger.warning(f'Response code is {response.status_code}')
        response.raise_for_status()
        key: str = response.json()['key']
        self.logger.info(f'Link received is {self.url}{key}')
        return self.url + key
