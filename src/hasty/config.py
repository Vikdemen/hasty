import configparser
import logging
from pathlib import Path
import re
from typing import Union

DEFAULT_URL = r'https://hastebin.com/'
CONFIG_FILENAME = 'config.ini'


def load_config(filepath: Union[str, Path] = CONFIG_FILENAME, absolute=False) -> str:
    """
    :return: URL in config.ini file or default URL
    """
    logger = logging.getLogger(__name__)
    if isinstance(filepath, str):
        filepath = Path(filepath)
    try:
        url = _load_from_file(filepath, absolute)
    except (KeyError, configparser.Error, FileNotFoundError) as ex:
        logger.debug(ex, exc_info=True)
        if isinstance(ex, KeyError) or isinstance(ex, configparser.Error):
            logger.warning('Url config file has wrong format, using default')
        elif isinstance(ex, FileNotFoundError):
            logger.warning('Url config file is not found, using default')
        return DEFAULT_URL
    else:
        if not _is_valid(url):
            logger.error(f'{url} is using invalid format, must be {DEFAULT_URL}, using default')
            return DEFAULT_URL
        logger.info(f"Config successfully loaded, url is {url}")
        return url


def _is_valid(url: str) -> bool:
    """
    :param url: URL string
    :return: If it conforms to https://hastebin.com/ format
    """
    url_pattern = r'(https?:\/\/)([A-z][A-z.-]*)(:\d+)?/'
    match = re.fullmatch(url_pattern, url)
    return match is not None


def _load_from_file(filepath: Path, absolute: bool) -> str:
    """
    :param filepath: Name of or path to config file in ini format
    :param absolute: If the path is not absolute, it's relative to script folder
    :return: URL from the config file
    :raises:
        FileNotFoundError: When the ini file is not found
        KeyError: When it lacks url field in DEFAULT section
    """
    if absolute:
        config_file = filepath
    else:
        config_file = Path(__file__) / filepath
    if not config_file.is_file():
        # configparser ignores not found files
        raise FileNotFoundError(f'Unable to find {config_file}')
    parser = configparser.ConfigParser()
    # noinspection PyTypeChecker
    # If filenames is a string, a bytes object or a path-like object, it is treated as a single filename.
    parser.read(filepath)
    url = parser['DEFAULT']['url']
    return url
