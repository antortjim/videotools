import cv2
import argparse
import numpy
import tqdm

ap = argparse.ArgumentParser()
ap.add_argument("--video")
ap.add_argument("--output")
args = ap.parse_args()

def invert(frame):
    return 255 - frame

def main():
    cap = cv2.VideoCapture(args.video)
    vw = None

    nframes = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(nframes)
    for i in tqdm.tqdm(range(nframes)):
        status, frame = cap.read()
        if vw is None:
            print("initializing video writer")
            res = tuple(frame.shape[:2][::-1])
            print(res)
            print(args.output)
            vw = cv2.VideoWriter(args.output, cv2.VideoWriter_fourcc(*"MJPG"), 20, res)
        if status is True:
            frame = invert(frame)
            vw.write(frame)
        else:
            cap.release()
            if not vw is None:
                vw.release()
            break


main()
