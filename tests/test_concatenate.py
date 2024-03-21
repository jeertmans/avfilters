import subprocess
import tempfile
from pathlib import Path
from typing import Iterable

import pytest

from avfilters import concatenate, inspect
from avfilters.inspect import filter_out_no_stream

from .utils import assert_equal_videos, random_video


def ffmpeg_concatenate(files: Iterable[str], dst: str) -> None:
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
        f.writelines(f"file '{file}'\n" for file in files)
        list_filename = f.name

    subprocess.check_call(
        [
            "ffmpeg",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            list_filename,
            "-c",
            "copy",
            dst,
            "-y",
        ],
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
def test_concatenate(format_: str, durations: Iterable[float], seed: int) -> None:
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

        stream = inspect(got.name)[0]

        assert stream.duration * stream.time_base == sum(durations)

        assert_equal_videos(got.name, expected.name)


def test_issue_manim_slides_390(issues_folder: Path):
    folder = issues_folder.joinpath("manim-slides-390")
    video_files = [folder.joinpath(f"{i}.mp4").as_posix() for i in range(5)]

    with tempfile.NamedTemporaryFile(
        delete=False, suffix=".mp4"
    ) as got, tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as expected:
        with pytest.raises(ValueError) as e:
            concatenate(video_files, got.name)
            assert (
                "Application provided invalid, non monotonically increasing dts to muxer in stream 0"
                in str(e)
            )

        video_files = list(filter_out_no_stream(video_files))
        concatenate(video_files, got.name)
        ffmpeg_concatenate(video_files, expected.name)
        assert_equal_videos(got.name, expected.name)
