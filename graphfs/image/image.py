from functools import cached_property
from typing import Any

from PIL import Image as PILImage, ExifTags as PILExifTags

from graphfs.file import File

class ImageFile(File):
    @cached_property
    def exif(self) -> dict[str, Any]:
        with PILImage.open(self.path) as image:
            # NOTE: ._getexif seems to return more info than .getexif
            raw_exif: dict[int, Any] = image._getexif()
        exif = { PILExifTags.TAGS[k]: v for k, v in raw_exif.items() }
        return exif
