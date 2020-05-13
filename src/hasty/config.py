import configparser
import logging
import pathlib

DEFAULT_URL = r'https://hastebin.com/'
CONFIG_FILENAME = 'config.ini'


def load_config() -> str:
    """
    :return: URL in config.ini file or default URL
    """
    logger = logging.getLogger(__name__)
    try:
        url = _load_from_file(CONFIG_FILENAME)
        logger.info(f'Settings successfully loaded, url is {url}')
    except FileNotFoundError:
        logger.exception('Url config file is not found, using default')
        url = DEFAULT_URL
    except ValueError:
        logger.exception('Url config file is invalid, using default')
        url = DEFAULT_URL
    return url


def _load_from_file(filename: str) -> str:
    """
    :param filename: Name of config file in ini format, seaches for it in the script folder
    :return: URL from the config file
    :raises:
        FileNotFoundError: When the ini file is not found
        ValueError: When it lacks url field in DEFAULT section
    """
    config_file = pathlib.Path(__file__).with_name(filename).resolve()
    parser = configparser.ConfigParser()
    parser.read(config_file)
    if not parser:
        # configparser ignores not found files
        raise FileNotFoundError(f'Unable to find {config_file}')
    try:
        url = parser['DEFAULT']['url']
        return url
    except KeyError as exc:
        raise ValueError(f'Url is not found in {config_file}', exc)
