"""
Routines to interact with image files
"""
import exif
import os

ON_PLEX_ATTR_NAME: str = "user.copied-to-plex"
ATTR_SET_VALUE: bytes = b"Yes"


def load_image(path: str) -> exif.Image:
    with open(path, "rb") as f:
        return exif.Image(f)


def get_dir_tree_from_path(path: str) -> (str, str):
    i: exif.Image = load_image(path)
    return get_dir_tree_from_image(i)


def get_dir_tree_from_image(image: exif.Image) -> (str, str):
    timestamp: str = image.datetime_original
    dt: str = timestamp.split(" ")[0]
    date_parts: [str] = dt.split(":")

    return date_parts[0], f"{date_parts[0]}{date_parts[1]}{date_parts[2]}"


def mark_copied_to_plex(path: str) -> bool:
    os.setxattr(path, ON_PLEX_ATTR_NAME, ATTR_SET_VALUE)
    return True


def has_extended_file_attr_set_to_yes(file_name: str, attr_name: str) -> bool:
    for n in os.listxattr(file_name):
        if n == attr_name and ATTR_SET_VALUE == os.getxattr(file_name, n):
            return True
    return False
