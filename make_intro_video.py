import argparse
import subprocess
import os

def extract_and_crop(video_file, start, end, output_file):
    """
    Extracts a section of a video and crops it to the largest centered square
    """
    ffmpeg_command = [
        "ffmpeg", "-y",
        "-i", video_file,
        "-ss", start,
        "-to", end,
        "-vf", "crop=in_h:in_h,scale=1024:1024",
        output_file
    ]

    subprocess.run(ffmpeg_command, check=True)

def create_concat_file(file_list, concat_file="concat_list.txt"):
    """
    Writes a list of files to a temporary text file for ffmpeg to use for concatenation
    """
    with open(concat_file, 'w') as f:
        for temp_file in file_list:
            f.write(f"file '{temp_file}'\n")
    return concat_file

def concatenate_videos(concat_file, output_file_path):
    """
    Uses ffmpeg to concatenate a list of videos together into one video
    """
    concat_command = [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", concat_file,
        #"-c", "copy",
        output_file_path,
    ]
    subprocess.run(concat_command, check=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--clips-txt", help="txt file with clip info", required=True)
    parser.add_argument("--output-video", help="Output video file name", required=True)

    args = parser.parse_args()

    video_file_path = args.clips_txt
    output_file_path = args.output_video

    with open(video_file_path, 'r') as f:
        lines = f.readlines()

    temp_files = []
    for i, line in enumerate(lines):
        video_file, start, end = line.strip("\n").split(',')
        temp_file = "temp_{:03d}.mkv".format(i)
        temp_files.append(temp_file)

        extract_and_crop(video_file, start, end, temp_file)

    concat_file_path = create_concat_file(temp_files)
    concatenate_videos(concat_file_path, output_file_path)

    # Clean up temp files.
    #for temp_file in temp_files:
    #    os.remove(temp_file)

    # Clean up concat list file.
    os.remove(concat_file_path)
