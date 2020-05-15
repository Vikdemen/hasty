import hasty.config
import pytest

from tests.conftest import File


@pytest.fixture
def test_config_file(tmp_path):
    text = r"""[DEFAULT]
url = https://paste.pythondiscord.com/"""
    filepath = tmp_path / 'test_config.ini'
    filepath.write_text(text)
    yield File(path=filepath, content=text)
    filepath.unlink()


def test_load_config(test_config_file):
    assert hasty.config.load_config(test_config_file.path) in test_config_file.content


def test_load_config_no_file():
    assert hasty.config.load_config('no_file.ini') == hasty.config.DEFAULT_URL


def test_load_config_invalid_format(fake_file):
    assert hasty.config.load_config(fake_file.path, absolute=True) == hasty.config.DEFAULT_URL
