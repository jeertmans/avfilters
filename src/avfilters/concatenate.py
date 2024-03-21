import tempfile
from typing import Iterable

import av


def concatenate(files: Iterable[str], dst: str) -> None:
    """Concatenate multiple media into a single media.

    Args:
        src: TODO.
        dst: The path to the destination file.
            Any existing file will be overwritten.
    """
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
        f.writelines(f"file '{file}'\n" for file in files)
        list_filename = f.name

    with av.open(
        list_filename, format="concat", options={"safe": "0"}
    ) as input_container, av.open(dst, mode="w") as output_container:
        input_stream = input_container.streams.video[0]
        output_stream = output_container.add_stream(
            template=input_stream,
        )

        for packet in input_container.demux(input_stream):
            if packet.dts is None:
                continue

            packet.stream = output_stream
            output_container.mux(packet)
