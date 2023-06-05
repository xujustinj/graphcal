from functools import cached_property
from typing import Any

from ffmpeg import probe

from graphfs.file import Value, File

from .util import is_video, same

class VideoFile(File):
    def __post_init__(self):
        super().__post_init__()
        assert is_video(self.path)

    @cached_property
    def metadata(self) -> dict[str, Any]:
        return probe(self.path)

    @cached_property
    def video_streams(self) -> list[dict[str, Any]]:
        return list(filter(
            lambda s: s["codec_type"] == "video",
            self.metadata["streams"],
        ))

    @cached_property
    def audio_streams(self) -> list[dict[str, Any]]:
        return list(filter(
            lambda s: s["codec_type"] == "audio",
            self.metadata["streams"],
        ))

    @cached_property
    def duration_seconds(self) -> float:
        return ("!!duration_seconds", same(float(s["duration"]) for s in self.video_streams))

    @cached_property
    def creation_time(self) -> float:
        return ("!!time", same(s["tags"]["creation_time"] for s in self.video_streams))

    @cached_property
    def width_pixels(self) -> int:
        return ("!!pixels", same(int(s["width"]) for s in self.video_streams))

    @cached_property
    def height_pixels(self) -> int:
        return ("!!pixels", same(int(s["height"]) for s in self.video_streams))

    @cached_property
    def properties(self) -> dict[str, Value]:
        return {
            **super().properties,
            "is_taken_at_time": self.creation_time,
            "has_width_pixels": self.width_pixels,
            "has_height_pixels": self.height_pixels,
            "has_duration_s": self.duration_seconds,
            # TODO: more cool properties
        }
