import configparser
import pathlib


class Config:
    CONFIG_FILE = pathlib.Path(__file__).parent.absolute()/'config.ini'

    def __init__(self, filepath=CONFIG_FILE):
        self.parser = configparser.ConfigParser()
        self.parser.read(filepath)
        self.url = self.parser['DEFAULT']['url']
