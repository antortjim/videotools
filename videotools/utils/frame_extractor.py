"""
Extract a list of frame numbers  from a video
"""
import argparse
import os.path

import cv2

ap=argparse.ArgumentParser()
ap.add_argument("--video", help="Path to video", type=str)
ap.add_argument("-s", "--frame-number", dest="frame_number", help="Position in video. 0 based", type=int, nargs="+")
args = ap.parse_args()

def main():

    cap = cv2.VideoCapture(args.video)
    def save(frame_number):
        filename = f"output_{frame_number}.png"
        if os.path.exists(filename):
            return 0

        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        stat, frame = cap.read()
        if stat:
            cv2.imwrite(filename, frame)
        return stat

    for frame_number in args.frame_number:
        save(frame_number)

    cap.release()
    return 0
    

if __name__ == "__main__":
    main()
