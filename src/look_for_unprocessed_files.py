import os
import sys

import images as img


def main() -> None:
    print()

    if len(sys.argv) != 2:
        print("INVALID COMMAND LINE.  EXACTLY ONE COMMAND LINE ARGUMENT EXPECTED.")
        print("Usage:  organize_photos_by_date_taken <DIRECTORY TO CHECK>")
        sys.exit(1)

    path: str = sys.argv[1]

    for current_dir, dirs, files in os.walk(path):
        dirs.sort()
        print(f"Processing: {current_dir}")

        for f in sorted(files):
            full_path: str = os.path.join(current_dir, f)
            if not img.has_extended_file_attr_set_to_yes(full_path, img.ON_PLEX_ATTR_NAME) \
               and not "Thumbs.db" == f:
                print(f"    {f}")
        print()


if __name__ == "__main__":
    main()
