import subprocess
import tempfile

import numpy as np
import pytest

from avfilters import reverse

from .utils import assert_equal_videos, random_video


def ffmpeg_reverse(src: str, dst: str) -> None:
    subprocess.check_call(
        [
            "ffmpeg",
            "-i",
            src,
            "-vf",
            "reverse",
            "-af",
            "reverse",
            dst,
            "-y",
        ],
    )


@pytest.mark.parametrize("format_", (".mp4", ".avi", ".mov"))
@pytest.mark.parametrize("duration", (1, 2, 10))
def test_reverse(format_: str, duration: float) -> None:
    video_file = random_video(
        1, format_=format_, duration=duration, fps=3, width=2, height=2
    ).as_posix()

    with tempfile.NamedTemporaryFile(
        delete=False, suffix=format_
    ) as got, tempfile.NamedTemporaryFile(delete=False, suffix=format_) as expected:
        reverse(video_file, got.name)
        ffmpeg_reverse(video_file, expected.name)
        assert_equal_videos(got.name, expected.name, atol=11, rtol=1e-1)


@pytest.mark.parametrize("format_", (".mp4", ".avi", ".mov"))
@pytest.mark.parametrize("color", (True, False))
def test_reverse_arange(format_: str, color: bool) -> None:
    video_file = random_video(
        "reverse_arange",
        format_=format_,
        color=color,
        fun=lambda i, size: np.full(size, fill_value=i, dtype=np.uint8),
    ).as_posix()

    with tempfile.NamedTemporaryFile(
        delete=False, suffix=format_
    ) as tmp, tempfile.NamedTemporaryFile(delete=False, suffix=format_) as got:
        reverse(video_file, tmp.name)
        reverse(tmp.name, got.name)
        assert_equal_videos(got.name, video_file)
