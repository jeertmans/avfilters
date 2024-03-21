import pytest

from .utils import assert_equal_videos, assert_not_equal_videos, random_video


def test_same_videos() -> None:
    video_1 = random_video(1)
    assert_equal_videos(str(video_1), str(video_1))


def test_different_seed_videos() -> None:
    video_1 = random_video(1)
    video_2 = random_video(2)
    assert_not_equal_videos(str(video_1), str(video_2))


def test_different_duration_videos() -> None:
    video_1 = random_video(1, duration=1)
    video_2 = random_video(1, duration=2)
    assert_not_equal_videos(str(video_1), str(video_2))


def test_different_fps_videos() -> None:
    video_1 = random_video(1, fps=25)
    video_2 = random_video(1, fps=30)
    assert_not_equal_videos(str(video_1), str(video_2))


def test_same_duration_fps_product_videos() -> None:
    video_1 = random_video(1, duration=2, fps=25)
    video_2 = random_video(1, duration=1, fps=50)
    assert_not_equal_videos(str(video_1), str(video_2))


def test_different_size_videos() -> None:
    video_1 = random_video(1, height=100, width=50)
    video_2 = random_video(1, height=50, width=100)
    assert_not_equal_videos(str(video_1), str(video_2))


def test_different_color_videos() -> None:
    video_1 = random_video(1, color=False)
    video_2 = random_video(1, color=True)
    assert_not_equal_videos(str(video_1), str(video_2))


@pytest.mark.xfail(reason="Remuxed videos are equal...")
def test_different_formats_videos() -> None:
    video_1 = random_video(1, format_=".mp4")
    video_2 = random_video(1, format_=".avi")
    assert_not_equal_videos(str(video_1), str(video_2))
