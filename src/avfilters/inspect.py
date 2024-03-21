"""
Multimedia files inspection utilities.
"""

from dataclasses import dataclass
from fractions import Fraction
from typing import Iterator, List

import av


@dataclass
class Codec:
    # TODO: complete missing fields
    name: str

    @classmethod
    def from_av_codec(cls, codec: av.Codec) -> "Codec":
        """
        Create a codec dataclass from a PyAV codec.

        Args:
            The PyAV codec.

        Return:
            The corresponding codec dataclass.
        """
        return cls(name=codec.name)


@dataclass
class CodecContext:
    # TODO: complete missing fields
    codec: Codec

    @classmethod
    def from_av_codec_context(cls, codec_context: av.CodecContext) -> "CodecContext":
        """
        Create a codec context dataclass from a PyAV codec context.

        Args:
            The PyAV codec context.

        Return:
            The corresponding codec context dataclass.
        """
        return cls(codec=Codec.from_av_codec(codec_context.codec))


@dataclass
class Stream:
    averaged_rate: Fraction
    base_rate: Fraction
    codec_context: CodecContext
    duration: float
    frames: int
    guessed_rate: Fraction
    index: int
    language: str
    metadata: dict
    profile: str
    start_time: str
    time_base: Fraction
    type: str

    @classmethod
    def from_av_stream(cls, stream: av.stream.Stream) -> "Stream":
        """
        Create a stream dataclass from a PyAV stream.

        Args:
            The PyAV stream.

        Return:
            The corresponding stream dataclass.
        """
        return cls(
            averaged_rate=stream.base_rate,
            base_rate=stream.base_rate,
            codec_context=CodecContext.from_av_codec_context(stream.codec_context),
            duration=stream.duration,
            frames=stream.frames,
            guessed_rate=stream.guessed_rate,
            index=stream.index,
            language=stream.language,
            metadata=stream.metadata,
            profile=stream.profile,
            start_time=stream.start_time,
            time_base=stream.time_base,
            type=stream.type,
        )

    @property
    def duration_seconds(self) -> float:
        """Return the duration of this stream in seconds.

        Return:
            The duration of this stream in seconds.
        """
        return float(self.duration * self.time_base)

@dataclass
class Container:
    streams: List[Stream]

    def __getitem__(self, key: int) -> Stream:
        """
        Return the stream at a given index.

        Return:
            The corresponding stream.
        """
        return self.streams[key]

    def __iter__(self) -> Iterator[Stream]:
        """
        Return an iterator over this container's streams.

        Return:
            An iterator over this container's streams.
        """
        return iter(self.streams)

    def __len__(self) -> int:
        """
        Return the number of streams in this container.

        Return:
            The number of streams.
        """
        return len(self.streams)

    @classmethod
    def from_file(cls, file) -> "Container":
        """
        Create a container dataclass from a multimedia file.

        Args:
            The multimedia file.

        Return:
            The corresponding container dataclass.
        """
        with av.open(file) as container:
            return Container.from_av_container(container)

    @classmethod
    def from_av_container(cls, container: av.container.Container) -> "Container":
        """
        Create a container from a PyAV container.

        Args:
            The PyAV container.

        Return:
            The corresponding container dataclass.
        """
        return cls(streams=[Stream.from_av_stream(stream) for stream in container.streams])
        

def inspect(file: str) -> Container:
    """
    Open (and close) a multimedia container for streams analysis.

    Args:
        The multimedia file.

    Return:
        The corresponding container dataclass.
    """
    return Container.from_file(file)


def filter_out_no_stream(files: Iterator[str]) -> Iterator[str]:
    """
    Return a iterator that excludes files with no stream.

    Args:
        The multimedia files.

    Return:
        The files that have at least one stream.
    """
    for file in files:
        with av.open(file) as container:
            if len(container.streams) > 0:
                yield file
