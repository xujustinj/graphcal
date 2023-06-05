import os
from typing import Iterator

from .file import File
from .image import ImageFile, is_image
from .video import VideoFile, is_video

def _graphfs_open_file(path) -> File:
    assert os.path.exists(path)
    assert os.path.isfile(path)

    if is_image(path):
        return ImageFile(path)
    elif is_video(path):
        return VideoFile(path)
    else:
        return File(path)

def graphfs_open(path) -> Iterator[File]:
    assert os.path.exists(path)

    if os.path.isdir(path):
        for subpath in os.listdir(path):
            yield from graphfs_open(os.path.join(path, subpath))
    else:
        yield _graphfs_open_file(path)
