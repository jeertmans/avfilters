import subprocess
import tempfile
from typing import List

import pytest

from avfilters.concatenate import concatenate

from .utils import equal_videos, random_video


@pytest.mark.parametrize("format_", (".mp4", ".avi", ".mov"))
@pytest.mark.parametrize(
    "durations,seed",
    (
        ([1, 1, 1], 0),
        ([1, 2, 3], 0),
        ([1, 1, 1, 1, 1, 1, 2], 1),
        ([1 for i in range(10)], 1),
    ),
)
def test_concatenate(format_: str, durations: List[float], seed: int) -> None:
    video_files = [
        random_video(
            seed if seed > 0 else i, duration=duration, format_=format_
        ).as_posix()
        for i, duration in enumerate(durations, start=1)
    ]

    with tempfile.NamedTemporaryFile(
        delete=False, suffix=".mp4"
    ) as got, tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as expected:
        concatenate(video_files, got.name)

        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
            f.writelines(f"file '{file}'\n" for file in video_files)
            f.close()
            subprocess.run(
                [
                    "ffmpeg",
                    "-f",
                    "concat",
                    "-safe",
                    "0",
                    "-i",
                    f.name,
                    "-c",
                    "copy",
                    expected.name,
                    "-y",
                ],
                check=True,
            )

        assert equal_videos(got.name, expected.name)
