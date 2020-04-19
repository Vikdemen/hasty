import configparser
import pathlib


class Config:
    CONFIG_FILE = pathlib.Path(__file__).parent.absolute()/'config.ini'

    def __init__(self, logger=None, filepath=CONFIG_FILE):
        self.parser = configparser.ConfigParser()
        self.logger = logger
        self.parser.read(filepath)
        try:
            self.url = self.parser['DEFAULT']['url']
        except KeyError:
            if self.logger is not None:
                logger.error('Url config is not found, using default')
            self.url = r'https://hastebin.com/'
