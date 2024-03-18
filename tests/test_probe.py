import pytest

from avfilters.probe import probe

from .utils import random_video


@pytest.mark.parametrize("duration", (1, 2, 10))
@pytest.mark.parametrize("fps", (1, 2, 10))
def test_probe(duration: float, fps: float):
    video = random_video(1, duration=duration, fps=fps)
    info = probe(str(video))

    stream = info[0]

    assert stream.frames == duration * fps
    assert float(stream.base_rate) == fps
