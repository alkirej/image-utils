import os
import shutil as shu
import subprocess as proc
import sys

import images as img

VALID_IMAGE_EXTENSIONS: [str] = ["jpg", "png", "gif"]
VALID_MOVIE_EXTENSIONS: [str] = ["mov", "mp4", "avi", "3gp", "3g2"]


def is_image_file(file_name: str) -> bool:
    for ext in VALID_IMAGE_EXTENSIONS:
        if file_name.lower().endswith(f".{ext}"):
            return True

    return False


def is_movie_file(file_name: str) -> bool:
    for ext in VALID_MOVIE_EXTENSIONS:
        if file_name.lower().endswith(f".{ext}"):
            return True

    return False


def copy_image_to_plex(plex_root: str, image_path: str) -> None:
    i = img.load_image(image_path)
    try:
        year_dir, day_dir = img.get_dir_tree_from_image(i)
    except KeyError:
        print(f"\n    **** Missing metadata.  Moving to Unknown Date folder. ({image_path})", end="")
        year_dir = "0000 Uncertain"
        day_dir = ""

    file_name: str = image_path.split("/")[-1]

    print(f" (to {day_dir})", end="")
    final_dir: str = os.path.join(plex_root, year_dir, day_dir)
    os.makedirs(final_dir, exist_ok=True)

    final_file_name: str = os.path.join(final_dir, file_name)
    shu.copy2(image_path, final_file_name)

    img.mark_copied_to_plex(image_path)


def copy_image_dir_to_plex(plex_root: str, image_root: str) -> None:
    for current_dir, dirs, files in os.walk(image_root):
        print(f"Processing: {current_dir}")
        dirs.sort()
        for f in sorted(files):
            if is_image_file(f):
                print(f"    Copying: {f}", end="")
                full_path: str = os.path.join(current_dir, f)
                if img.has_extended_file_attr_set_to_yes(full_path, img.ON_PLEX_ATTR_NAME):
                    print("  Already done.")
                else:
                    image_path: str = os.path.join(current_dir, f)
                    copy_image_to_plex(plex_root, image_path)
                    print()
            elif is_movie_file(f):
                print(f"    Processing: {f}", end="")
                plex_dir: str = os.path.join(plex_root, "../Video/Home-Movies")
                movie_path: str = os.path.join(current_dir, f)
                if img.has_extended_file_attr_set_to_yes(movie_path, img.ON_PLEX_ATTR_NAME):
                    print("  Already done.")
                else:
                    print("   ***********************************")
                    encode_args: [str] = ["python",
                                          "/home/jeff/git/image-utils/src/encode_camera_video.py",
                                          plex_dir,
                                          movie_path
                                          ]
                    results = proc.run(encode_args)

                    if results.returncode != 0:
                        print(f"Return code from encode_camera_video.py was {results.returncode}. Exiting")
                        sys.exit(1)

                    img.mark_copied_to_plex(movie_path)

        print()


def main() -> None:
    print()

    if len(sys.argv) != 3:
        print("INVALID COMMAND LINE.  EXACTLY TWO COMMAND LINE ARGUMENT EXPECTED.")
        print("Usage:  organize_photos_by_date_taken <DIRECTORY WITH IMAGES> <DIRECTORY ON PLEX SERVER>")
        sys.exit(1)

    path_to_process: str = sys.argv[1]
    if not os.path.isdir(path_to_process):
        print(f"{path_to_process} was not found or is not a directory.")
        sys.exit(1)

    plex_dir: str = sys.argv[2]
    if not os.path.isdir(path_to_process):
        print(f"{plex_dir} was not found or is not a directory.")
        sys.exit(1)

    copy_image_dir_to_plex(plex_dir, path_to_process)
    print(f"FROM: {path_to_process}")
    print(f"TO:   {plex_dir}")


if __name__ == "__main__":
    main()
