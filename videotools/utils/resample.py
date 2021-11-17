import argparse
import os.path

import tqdm
import cv2
import math


def get_parser():
    ap = argparse.ArgumentParser()
    ap.add_argument("--video", type=str, required=True)
    ap.add_argument("--framerate", type=int, required=True)
    ap.add_argument("--output", type=str, required=True)
    ap.add_argument("-t", type=str, dest="t")
    return ap


def main(args=None):

    if args is None:
        ap = get_parser()
        args = vars(ap.parse_args())

    cap = cv2.VideoCapture(args["video"])
    nframes = cap.get(7)
    fps = cap.get(5)
    pb = tqdm.tqdm(total=nframes)
    video_writer = None

    ret = True

    if args["t"] is None:
        last_frame = math.inf
    else:
        end_time = args["t"].split(":")
        end_time = [int(e) for e in end_time]
        end_time_s = end_time[0] * 3600 + end_time[1] * 60 + end_time[2]
        last_frame = end_time_s * fps

    i = 0
    while ret:
        ret, frame = cap.read()
        if not ret:
            break
        pb.update(1)

        resolution = frame.shape[:2][::-1]

        extension = os.path.splitext(args["output"])[1]
        if extension == ".avi":
            codec = cv2.VideoWriter_fourcc(*"DIVX")
        elif extension == ".mp4":
            codec = cv2.VideoWriter_fourcc(*"mp4v")
        else:
            raise Exception("Unsupported output format")


        if video_writer is None:
            video_writer = cv2.VideoWriter(
                args["output"],
                codec,
                args["framerate"],
                resolution
            )

        video_writer.write(frame)
        i += 1
        if i == last_frame:
            break

    cap.release()
    video_writer.release()

if __name__ == "__main__":
    main()
