import shutil
from pathlib import Path

import pytest

from mmw_data.validate import DATABASE_CSV
from tests.test_validate import DATA


@pytest.fixture
def data(tmp_path: Path) -> Path:
    d = tmp_path / "data"
    d.mkdir()
    shutil.copy(DATA / DATABASE_CSV, d)
    for folder in DATA.glob("0[1-6]_*"):
        shutil.copytree(folder, d / folder.name)
    return d
