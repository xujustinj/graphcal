import os

# NOTE: we use PIL, which supports far more than just these formats
# https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html
IMAGE_EXTENSIONS = {".jpeg", ".jpg", ".png"}

def is_image(path: str) -> bool:
    _, ext = os.path.splitext(path)
    return ext.lower() in IMAGE_EXTENSIONS
