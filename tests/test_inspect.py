import pytest

from avfilters import inspect

from .utils import random_video


@pytest.mark.parametrize("duration", (1, 2, 10))
@pytest.mark.parametrize("fps", (1, 2, 10))
def test_inspect(duration: float, fps: float):
    video = random_video(1, duration=duration, fps=fps)
    container = inspect(str(video))

    stream = container.streams[0]

    assert stream.frames == duration * fps
    assert stream.duration_seconds == duration
    assert float(stream.base_rate) == fps
