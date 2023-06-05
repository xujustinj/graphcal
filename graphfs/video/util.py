import os
from typing import Iterable, TypeVar

# NOTE: we use ffmpeg, which supports far more than just these formats
# https://www.ffmpeg.org/ffmpeg-formats.html
VIDEO_EXTENSIONS = {".mov", ".mp4"}

def is_video(path: str) -> bool:
    _, ext = os.path.splitext(path)
    return ext.lower() in VIDEO_EXTENSIONS

T = TypeVar("T")
def same(l: Iterable[T]) -> T:
    for first in l:
        break
    for t in l:
        assert t == first
    return first
