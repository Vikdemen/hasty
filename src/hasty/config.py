import configparser

_DEFAULT_URL = r'https://hastebin.com/'


def _url_from_config() -> str:
    try:
        config = configparser.ConfigParser()
        config.read('example.ini')
        url = config['DEFAULT']['url']
        return url
    except (IOError, KeyError):
        return _DEFAULT_URL


_from_config = _url_from_config()
HASTEBIN_URL = _from_config
