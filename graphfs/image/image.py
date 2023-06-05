from functools import cached_property
from typing import Any

from PIL import Image as PILImage, ExifTags as PILExifTags

from graphfs.file import Value, File
from graphfs.value import Camera, Time

from .util import is_image

GPS_INFO = "GPSInfo"

class ImageFile(File):
    def __post_init__(self):
        super().__post_init__()
        assert is_image(self.path)

    @cached_property
    def exif(self) -> dict[str, Any]:
        with PILImage.open(self.path) as image:
            # NOTE: ._getexif seems to return more info than .getexif
            raw_exif: dict[int, Any] = image._getexif()

        exif = {}
        for k, v in raw_exif.items():
            if k == 59933:
                # HACK: see https://exiftool.org/standards.html
                tag = "Microsoft.OffsetSchema"
            else:
                tag = PILExifTags.TAGS.get(k)
            if tag is None:
                print(f"[{self.path}] WARNING: skipping unsupported EXIF tag ID {k}")
            exif[tag] = v

        # decompose GPSInfo into its component tags
        if GPS_INFO in exif:
            for k, v in exif.pop(GPS_INFO).items():
                exif[f"{GPS_INFO}.{PILExifTags.GPSTAGS[k]}"] = v

        return exif

    @cached_property
    def time(self) -> Value:
        datetime = self.exif.get("DateTime")
        assert datetime is None or isinstance(datetime, str)
        return Time(datetime)

    @cached_property
    def camera(self) -> Value:
        make = self.exif.get("Make")
        assert make is None or isinstance(make, str)

        model = self.exif.get("Model")
        assert model is None or isinstance(model, str)

        return Camera(make, model)

    @cached_property
    def properties(self) -> dict[str, Value]:
        return {
            **super().properties,
            "is_taken_at_time": self.time,
            "is_taken_by_camera": self.camera,
            # TODO: more cool properties
        }
