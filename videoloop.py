import subprocess
import argparse
import os

def reverse_and_concat(input_video, output_video):
    # Reverse video
    reverse_command = f'ffmpeg -i {input_video} -vf reverse -af areverse reversed.mp4'
    subprocess.call(reverse_command, shell=True)

    # write concat file
    with open("concat.txt","w") as f:
        f.write("file '" + input_video + "'\n")
        f.write("file 'reversed.mp4'\n")
    
    # Concatenate
    #concat_command = f'ffmpeg -f concat -i concat.txt  {output_video}'
    concat_command = f'ffmpeg -f concat -i concat.txt  -vcodec libx264 -crf 28 {output_video}'
    subprocess.call(concat_command, shell=True)

    # Delete temporary reversed.mp4 and concat.txt
    os.remove("reversed.mp4")
    os.remove("concat.txt")

def main():
    # Set up command line parameters
    parser = argparse.ArgumentParser(description="Reverse and concatenate a video.")
    parser.add_argument("--input-video", type=str, help="Input video file path.")
    parser.add_argument("--output-video", type=str, help="Output video file path.")
    args = parser.parse_args()

    reverse_and_concat(args.input_video, args.output_video)

if __name__ == "__main__":
    main()
