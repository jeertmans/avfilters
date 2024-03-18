import sys

import pytest
import tempfile

from functools import partial


@pytest.fixture(autouse=True)
def patch_named_temporary_file(monkeypatch: pytest.MonkeyPatch) -> None:
    if sys.platform == "win32":
        # https://github.com/pypa/pip-audit/issues/646
        original = tempfile.NamedTemporaryFile

        monkeypatch.setattr(tempfile, "NamedTemporaryFile", partial(original, delete=False))
