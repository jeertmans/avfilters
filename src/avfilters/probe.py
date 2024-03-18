from dataclasses import dataclass
from fractions import Fraction

import av


@dataclass
class Codec:
    # TODO: complete missing fields
    name: str

    @classmethod
    def from_av_codec(cls, codec: av.Codec) -> "Codec":
        return cls(name=codec.name)


@dataclass
class CodecContext:
    # TODO: complete missing fields
    codec: Codec

    @classmethod
    def from_av_codec_context(cls, codec_context: av.CodecContext) -> "CodecContext":
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


def probe(file: str) -> list[Stream]:
    with av.open(file) as container:
        return [Stream.from_av_stream(stream) for stream in container.streams]
