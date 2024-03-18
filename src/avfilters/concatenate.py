import tempfile
from typing import Sequence

import av


def concatenate(files: Sequence[str], dest: str) -> None:
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt") as f:
        f.writelines(f"file '{file}'\n" for file in files)
        f.flush()

        input_container = av.open(f.name, format="concat", options={"safe": "0"})
        input_stream = input_container.streams.video[0]
        output_container = av.open(dest, mode="w")
        output_stream = output_container.add_stream(
            template=input_stream,
        )

        for packet in input_container.demux(input_stream):
            # We need to skip the "flushing" packets that `demux` generates.
            if packet.dts is None:
                continue

            # We need to assign the packet to the new stream.
            packet.stream = output_stream
            output_container.mux(packet)

        input_container.close()
        output_container.close()
