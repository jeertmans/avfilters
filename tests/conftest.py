from pathlib import Path

import pytest


@pytest.fixture
def tests_folder() -> Path:
    return Path(__file__).parent


@pytest.fixture
def issues_folder(tests_folder: Path) -> Path:
    return tests_folder.joinpath("issues")
