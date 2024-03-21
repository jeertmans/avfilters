import hashlib
from itertools import zip_longest
from pathlib import Path
from typing import Any, Callable, Optional, Tuple, Union

import av
import numpy as np
import pytest

from avfilters import inspect

MEDIA_FOLDER = Path(__file__).parent / "media"


def random_video(
    seed: Union[int, str],
    width: int = 854,
    height: int = 480,
    duration: float = 1.0,
    fps: float = 25.0,
    audio: bool = False,
    color: bool = True,
    format_=".mp4",
    *,
    fun: Optional[Callable[[int, Tuple[int, ...]], np.ndarray]] = None,
    cached: bool = True,
) -> Path:
    # TODO: add audio generation
    args = (seed, width, height, duration, fps, audio, color)
    basename = hashlib.sha256(repr(args).encode()).hexdigest()
    filename = MEDIA_FOLDER.joinpath(basename + format_)

    if filename.exists() and cached:
        return filename

    if not MEDIA_FOLDER.exists():
        MEDIA_FOLDER.mkdir(exist_ok=True)

    size = (height, width, 3) if color else (height, width)

    if not filename.exists():
        with av.open(str(filename), mode="w") as container:
            stream = container.add_stream("mpeg4", rate=fps)
            stream.width = width
            stream.height = height
            stream.pix_fmt = "yuv420p"

            if isinstance(seed, int) or fun is None:
                rng = np.random.default_rng(seed=seed)

                def fun(i: int, size: Tuple[int, ...]) -> np.ndarray:
                    return rng.integers(0, 256, size=size, dtype=np.uint8)

            for i in range(int(fps * duration)):
                array = fun(i, size)

                if color:
                    frame = av.VideoFrame.from_ndarray(array, format="rgb24")
                else:
                    frame = av.VideoFrame.from_ndarray(array, format="gray")

                for packet in stream.encode(frame):
                    container.mux(packet)

            for packet in stream.encode():
                container.mux(packet)

    return filename


def assert_equal_videos(video_1: str, video_2: str, **kwargs: Any) -> None:
    container_1 = inspect(video_1)
    container_2 = inspect(video_2)

    for stream_1, stream_2 in zip_longest(container_1, container_2):
        assert (stream_1 is None) == (stream_2 is None)
        assert stream_1.duration_seconds == stream_2.duration_seconds

    del container_1, container_2

    with av.open(video_1) as container_1, av.open(video_2) as container_2:
        for frame_1, frame_2 in zip_longest(
            container_1.decode(video=0), container_2.decode(video=0)
        ):
            assert (frame_1 is None) == (frame_2 is None)

            array_1 = frame_1.to_ndarray(format="rgb24")
            array_2 = frame_2.to_ndarray(format="rgb24")

            np.testing.assert_allclose(array_1, array_2, **kwargs)


def assert_not_equal_videos(video_1: str, video_2: str, **kwargs: Any) -> None:
    with pytest.raises(AssertionError):
        assert_equal_videos(video_1, video_2, **kwargs)
