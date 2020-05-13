from pathlib import Path
from typing import NamedTuple

import pytest


class File(NamedTuple):
    path: Path
    content: str


@pytest.fixture
def fake_file(tmp_path):
    text = 'Text from file'
    fake_filepath = tmp_path / 'fakefile.txt'
    fake_filepath.write_text(text)
    yield File(path=fake_filepath, content=text)
    fake_filepath.unlink()
