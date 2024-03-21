"""Multimedia files concatenation utilities."""

import tempfile
from typing import Iterable

import av


def concatenate(files: Iterable[str], dst: str) -> None:
    """Concatenate multiple media into a single media.

    Roughly equivalent to:

    .. code-block:: bash

       ffmpeg -f concat -safe 0 -i list.txt -c copy dst

    Where ``list.txt`` contains the list of files to concatenate.
    It will be automatically created in a temporary file.

    Args:
        files: The files that should be concatenated.

            All files must have the same streams
            (same codecs, same time base, etc.)
        dst: The path to the destination file.
            Any existing file will be overwritten.
    """
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
        f.writelines(f"file '{file}'\n" for file in files)
        list_filename = f.name

    with av.open(
        list_filename, format="concat", options={"safe": "0"}
    ) as input_container, av.open(dst, mode="w") as output_container:
        # TODO: check if (1) this works with audio and (2)
        # if we should rather iterate of streams?
        input_stream = input_container.streams.video[0]
        output_stream = output_container.add_stream(
            template=input_stream,
        )

        for packet in input_container.demux(input_stream):
            if packet.dts is None:
                continue

            packet.stream = output_stream
            output_container.mux(packet)
