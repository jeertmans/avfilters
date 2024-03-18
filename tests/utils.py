import hashlib
import logging
import subprocess
from itertools import zip_longest
from pathlib import Path

import av
import cv2
import numpy as np

MEDIA_FOLDER = Path(__file__).parent / "media"

logger = logging.getLogger(__name__)


def random_video(
    seed: int,
    width: int = 854,
    height: int = 480,
    duration: float = 1.0,
    fps: float = 25.0,
    audio: bool = False,
    color: bool = True,
    format_=".mp4",
    *,
    cached: bool = True,
) -> Path:
    args = (seed, width, height, duration, fps, audio, color)
    basename = hashlib.sha256(repr(args).encode()).hexdigest()
    filename_mp4 = MEDIA_FOLDER.joinpath(basename + ".mp4")
    filename = filename_mp4.with_suffix(format_)

    if filename.exists() and cached:
        logger.info("Random video already exists, skipping.")
        return filename

    if not MEDIA_FOLDER.exists():
        MEDIA_FOLDER.mkdir()

    size = (height, width, 3) if color else (height, width)

    if not filename_mp4.exists():
        logger.info("Generating random (MP4) video file.")
        output = cv2.VideoWriter(
            str(filename_mp4),
            cv2.VideoWriter_fourcc(*"mp4v"),
            fps,
            (width, height),
            color,
        )

        rng = np.random.default_rng(seed=seed)

        for _ in range(int(fps * duration)):
            frame = rng.integers(0, 256, size=size, dtype=np.uint8)
            output.write(frame)

        output.release()

    if filename.suffix != filename_mp4.suffix and (not filename.exists() or not cached):
        logger.info(f"Converting video file to specified format: {format_}.")
        process = subprocess.Popen(
            ["ffmpeg", "-i", str(filename_mp4), str(filename)], stdout=subprocess.PIPE
        )
        process.communicate()

        if not filename.exists() or process.returncode != 0:
            filename.unlink(missing_ok=True)
            raise ValueError(
                f"Could not convert the MP4 file to {format_}, cleaning file."
            )

    return filename


def equal_videos(video_1: str, video_2: str) -> bool:
    with av.open(video_1) as container_1, av.open(video_2) as container_2:
        for frame_1, frame_2 in zip_longest(
            container_1.decode(video=0), container_2.decode(video=0)
        ):
            if frame_1 is None or frame_2 is None:
                logger.info("Videos do not have the same number of frames.")
                return False

            array_1 = frame_1.to_ndarray()
            array_2 = frame_2.to_ndarray()
            if not np.array_equal(array_1, array_2):
                logger.info("Video frames are not equal.")
                return False

    return True
