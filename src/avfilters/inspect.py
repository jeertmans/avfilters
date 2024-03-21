"""Multimedia files inspection utilities.

This module is currently work in progress.
"""

from dataclasses import dataclass
from fractions import Fraction
from typing import Iterable, Iterator, List

import av


@dataclass
class Codec:  # TODO: complete missing fields
    """A codec.

    Dataclass version of :class:`av.Codec`.
    """

    name: str
    """The codec name."""

    @classmethod
    def from_av_codec(cls, codec: av.Codec) -> "Codec":
        """Create a codec dataclass from a PyAV codec.

        Args:
            codec: The PyAV codec.

        Return:
            The corresponding codec dataclass.
        """
        return cls(name=codec.name)


@dataclass
class CodecContext:  # TODO: complete missing fields
    """A codec context.

    Dataclass version of :class:`av.codec.context.CodecContext`.
    """

    codec: Codec
    """The codec."""

    @classmethod
    def from_av_codec_context(
        cls, codec_context: av.codec.context.CodecContext
    ) -> "CodecContext":
        """Create a codec context dataclass from a PyAV codec context.

        Args:
            codec_context: The PyAV codec context.

        Return:
            The corresponding codec context dataclass.
        """
        return cls(codec=Codec.from_av_codec(codec_context.codec))


@dataclass
class Stream:
    """A single stream of audio, video or subtitles within a Container.

    Dataclass version of :class:`av.stream.Stream`.
    """

    averaged_rate: Fraction
    """The average frame rate of this video stream.

    See :attr:`av.stream.Stream.averaged_rate`.
    """
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
    """The type of the stream.

    See :attr:`av.stream.Stream.type`.
    """

    @classmethod
    def from_av_stream(cls, stream: av.stream.Stream) -> "Stream":
        """Create a stream dataclass from a PyAV stream.

        Args:
            stream: The PyAV stream.

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
    """A multimedia container.

    Dataclass version of :class:`av.container.Container`.
    """

    """
    The list of streams in this container.
    """
    streams: List[Stream]

    def __getitem__(self, key: int) -> Stream:
        """Return the stream at a given index.

        Args:
            key: The index of the stream.

        Return:
            The corresponding stream.
        """
        return self.streams[key]

    def __iter__(self) -> Iterator[Stream]:
        """Return an iterator over this container's streams.

        Return:
            An iterator over this container's streams.
        """
        return iter(self.streams)

    def __len__(self) -> int:
        """Return the number of streams in this container.

        Return:
            The number of streams.
        """
        return len(self.streams)

    @classmethod
    def from_file(cls, file: str) -> "Container":
        """Create a container dataclass from a multimedia file.

        Args:
            file: The multimedia file.

        Return:
            The corresponding container dataclass.
        """
        with av.open(file) as container:
            return Container.from_av_container(container)

    @classmethod
    def from_av_container(cls, container: av.container.Container) -> "Container":
        """Create a container from a PyAV container.

        Args:
            container: The PyAV container.

        Return:
            The corresponding container dataclass.
        """
        return cls(
            streams=[Stream.from_av_stream(stream) for stream in container.streams]
        )


def inspect(file: str) -> Container:
    """Inpsect a multimedia file container.

    Args:
        file: The multimedia file.

    Return:
        The corresponding container dataclass.
    """
    return Container.from_file(file)


def filter_out_no_stream(files: Iterable[str]) -> Iterator[str]:
    """Return a iterator that excludes files with no stream.

    Args:
        files: The multimedia files.

    Return:
        The files that have at least one stream.
    """
    for file in files:
        with av.open(file) as container:
            if len(container.streams) > 0:
                yield file
