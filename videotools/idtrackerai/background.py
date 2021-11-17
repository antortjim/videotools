import argparse
import re
import os
import os.path

import numpy as np
import cv2
import tqdm

def get_parser():

    ap = argparse.ArgumentParser()
    ap.add_argument("--experiment-folder", dest="experiment_folder", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--interval", type=int, nargs="+", required=False, default=None)
    ap.add_argument("--ROI", dest="roi", required=False)
    return ap


def main(args=None):

    if args is None:
        ap = get_parser()
        args = ap.parse_args()


    files = os.listdir(args.experiment_folder)
    png_files = [f for f in files if os.path.splitext(f)[1] == ".png"]

    if len(png_files) == 0:
        raise Exception("No png files found!")

    shot_files = sorted([f for f in png_files if re.search("[0-9]{6}.png", os.path.basename(f))])
    if len(shot_files) == 0:
        raise Exception("No shot files found!")


    if not args.interval is None:
        start = args.interval[0]
        end = args.interval[1]
        shot_files = shot_files[start:end]

    import ipdb; ipdb.set_trace()
    shots = []
    for f in tqdm.tqdm(shot_files, desc="Loading shots to RAM..."):
        frame = cv2.imread(os.path.join(args.experiment_folder, f))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        shots.append(frame)

    print("Computing median image. This may take a while ...")
    background = np.median(np.stack(shots), axis=0)
    print("Done!")
    background_img = background.astype(np.uint8)
    cv2.imwrite(args.output, background_img)


if __name__ == "__main__":
    main()

