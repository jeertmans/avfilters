"""Multimedia files reversing utilities."""

import av


def reverse(src: str, dst: str) -> None:
    """Reverse a media.

    Roughly equivalent to:

    .. code-block:: bash

       ffmpeg -i src -vf reverse -af areverse dst

    Args:
        src: The path to the source file.
            The file must exist and be a valid media.
        dst: The path to the destination file.
            Any existing file will be overwritten.
    """
    with av.open(src) as input_container, av.open(dst, mode="w") as output_container:
        # TODO: check if (1) we can have multiple video streams, (2) if this works with
        # audio, and (3) we need to skip subtitle streams
        for input_stream in input_container.streams:
            output_stream = output_container.add_stream(
                input_stream.codec_context.name,
                rate=input_stream.base_rate,
            )
            output_stream.width = input_stream.codec_context.width
            output_stream.height = input_stream.codec_context.height
            output_stream.pix_fmt = input_stream.codec_context.pix_fmt

            graph = av.filter.Graph()

            nodes = [
                graph.add_buffer(template=input_stream),
                graph.add("reverse"),
                graph.add("buffersink"),
            ]

            for node_from, node_to in zip(nodes[:-1], nodes[+1:]):
                node_from.link_to(node_to)

            graph.configure()

            frames_count = 0
            for frame in input_container.decode(input_stream):
                graph.push(frame)
                frames_count += 1

            graph.push(None)  # EOF: https://github.com/PyAV-Org/PyAV/issues/886.

            for _ in range(frames_count):
                frame = graph.pull()

                for packet in output_stream.encode(frame):
                    output_container.mux(packet)

            for packet in output_stream.encode():
                output_container.mux(packet)
