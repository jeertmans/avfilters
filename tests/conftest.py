import sys

import pytest

from functools import partial


@pytest.fixture(autouse=True)
def patch_named_temporary_file(monkeypatch: pytest.MonkeyPatch) -> None:
    if sys.platform == "win32":
        from tempfile import NamedTemporaryFile

        monkeypatch.setattr("tempfile", "NamedTemporaryFile", partial(NamedTemporaryFile, delete=False))
