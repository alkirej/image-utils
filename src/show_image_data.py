import os
from PIL import Image, ExifTags
import sys

VALID_IMAGE_EXTENSIONS: [str] = [".jpg", ".png", ".gif"]


def display_image_metadata(metadata) -> None:
    if metadata is None or len(metadata) <= 0:
        print("    No metadata found in this image file.")
    else:
        for key in metadata:
            value = metadata[key]
            if key in ExifTags.TAGS:
                print(f"   {ExifTags.TAGS[key]} = {value}")
            else:
                print(f"   {key} = {value}")


def main() -> None:
    print()

    if len(sys.argv) != 2:
        print("INVALID COMMAND LINE.  EXACTLY ONE COMMAND LINE ARGUMENT EXPECTED.")
        print("    Usage:  python show_image_data.py <IMAGE FILE>")
        sys.exit(1)

    image_path: str = sys.argv[1]
    extension: str = image_path[-4:].lower()

    if extension not in VALID_IMAGE_EXTENSIONS and False:
        print("INVALID FILE EXTENSION.  NOT AN ACCEPTED IMAGE FORMAT.")
        print("    Usage:  python show_image_data.py <IMAGE FILE>")
        sys.exit(1)

    if not os.path.exists(image_path):
        print("CANNOT FIND A FILE AT THIS PATH.")
        print("    Usage:  python show_image_data.py <IMAGE FILE>")
        sys.exit(1)

    if os.path.isdir(image_path):
        print("EXPECTING AN IMAGE FILE, BUT FOUND A DIRECTORY.")
        print("    Usage:  python show_image_data.py <IMAGE FILE>")
        sys.exit(1)

    img = Image.open(image_path)
    if extension.lower() == ".jpg":
        metadata = img.getexif().items()
        display_image_metadata(metadata)

    elif extension.lower() == ".png":
        img.load()
        display_image_metadata(img.info)

    print()


if __name__ == "__main__":
    main()
