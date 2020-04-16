"""
Python alternative for haste-client CLI utility
"""
import requests
from hasty import cli

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
            raise requests.HTTPError()


def main(argv):
    get_text, show_link = cli.get_io(argv)
    url = r'https://hastebin.com/'
    # TODO - read from ini file
    text = get_text()
    hastebin = Hastebin(url)
    try:
        text_link = hastebin.paste(text)
    except requests.HTTPError:
        print('Service is unavailable')
    else:
        show_link(text_link)
