import subprocess
import tempfile
from pathlib import Path
from typing import Iterator

import pytest

from avfilters import concatenate, probe

from .utils import assert_equal_videos, random_video


def ffmpeg_concatenate(files: Iterator[str], dest: str) -> None:
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
        f.writelines(f"file '{file}'\n" for file in files)
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
                dest,
                "-y",
            ],
            check=True,
        )


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
def test_concatenate(format_: str, durations: Iterator[float], seed: int) -> None:
    video_files = [
        random_video(
            seed if seed > 0 else i, duration=duration, format_=format_
        ).as_posix()
        for i, duration in enumerate(durations, start=1)
    ]

    with tempfile.NamedTemporaryFile(
        delete=False, suffix=format_
    ) as got, tempfile.NamedTemporaryFile(delete=False, suffix=format_) as expected:
        concatenate(video_files, got.name)
        ffmpeg_concatenate(video_files, expected.name)

        assert_equal_videos(got.name, expected.name)


def test_issue_manim_slides_390(issues_folder: Path):
    folder = issues_folder.joinpath("manim-slides-390")

    video_files = [folder.joinpath(f"{i}.mp4") for i in range(5)]

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as got:
        concatenate(video_files, got.name)

        info = probe(got.name)
        assert len(info) == 1

        stream = info[0]

        assert stream.duration == 1
