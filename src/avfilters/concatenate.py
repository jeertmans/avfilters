import tempfile
from typing import Iterator

import av


def concatenate(files: Iterator[str], dest: str) -> None:
    """Concatenate a sequence of media into a single media."""
    with tempfile.NamedTemporaryFile(
        mode="w", delete=False, suffix=".txt"
    ) as f, av.open(
        f.name, format="concat", options={"safe": "0"}
    ) as input_container, av.open(dest, mode="w") as output_container:
        f.writelines(f"file '{file}'\n" for file in files)
        f.close()

        input_stream = input_container.streams.video[0]
        output_stream = output_container.add_stream(
            template=input_stream,
        )

        for packet in input_container.demux(input_stream):
            if packet.dts is None or packet.pts < 0:
                continue

            packet.stream = output_stream
            output_container.mux(packet)
