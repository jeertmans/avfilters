import tempfile
from typing import Sequence

import av


def concatenate(files: Sequence[str], dest: str) -> None:
    with tempfile.NamedTemporaryFile(mode="w", delete_on_close=False) as f:
        f.writelines(f"file '{file}'" for file in files)
        f.close()

        input_container = av.open(f.name, format="concat")
        input_audio_stream = input_container.streams.audio[0]
        input_video_stream = input_container.streams.video[0]

        for packet in input_container.demux(input_audio_stream, input_video_stream):
            pass
