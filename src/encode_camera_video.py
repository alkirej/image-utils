import ffmpeg
import os
import subprocess as proc
import sys

FFMPEG_FILE = "ffmpeg"


def main() -> None:
    if len(sys.argv) != 3:
        print("INVALID COMMAND LINE.  EXACTLY TWO COMMAND LINE ARGUMENT EXPECTED.")
        print("Usage:  python encode_camera_video.py <DIR WITHIN PLEX OR HOME VIDEOS> <FULL PATH TO MEDIA FILE>")
        sys.exit(1)

    plex_library_loc: str = sys.argv[1]
    media_file: str = sys.argv[2]

    # uses ffprobe command to extract all possible metadata from the media file
    try:
        full_creation_date: str = ffmpeg.probe(media_file)["format"]["tags"]["creation_time"]
    except KeyError:
        print(f"Did not process {media_file}")
        sys.exit(0)

    year: str = f"{full_creation_date[0:4]}"
    month: str = f"{full_creation_date[5:7]}"
    day: str = f"{full_creation_date[8:10]}"

    hour: str = f"{full_creation_date[11:13]}"
    minute: str = f"{full_creation_date[14:16]}"
    second: str = f"{full_creation_date[17:19]}"

    file_name: str = f"{year}{month}{day}-{hour}{minute}{second}.mkv"
    dir_path: str = os.path.join(plex_library_loc, year)
    new_file_path: str = os.path.join(dir_path, file_name)

    os.makedirs(dir_path, exist_ok=True)

    print(full_creation_date)
    print(file_name)

    # convert video file to h.265 to save space
    ffmpeg_args: [str] = ["nice",
                          FFMPEG_FILE,
                          "-y",
                          "-i", media_file,
                          "-c:v", "libx265",
                          "-c:a", "ac3",
                          new_file_path
                          ]

    results = proc.run(ffmpeg_args)
    if results.returncode != 0:
        print(f"Error transcoding file. ({results.returncode})")
        
    # nice ffmpeg -i MVI_9729.MOV -c:v libx265 -c:a ac3 mvi__9729.mkv


if __name__ == "__main__":
    main()
