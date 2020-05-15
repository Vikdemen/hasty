import hasty.config


def test_load_config(test_config_file):
    assert hasty.config.load_config(test_config_file.path) in test_config_file.content


def test_load_config_no_file():
    assert hasty.config.load_config('no_file.ini') == hasty.config.DEFAULT_URL


def test_load_config_invalid_format(fake_file):
    assert hasty.config.load_config(fake_file.path, relative=True) == hasty.config.DEFAULT_URL
