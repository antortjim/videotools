import argparse
import tqdm
import numpy as np
import cv2


def get_parser():
    ap = argparse.ArgumentParser()
    ap.add_argument("--video", "--input", dest="input", required=True, type=str)
    ap.add_argument("--output", required=True, type=str)
    ap.add_argument("--roi", help="XxY+W+H", required=False, type=str)
    ap.add_argument("--idtrackerai-conf", dest="idtrackerai_conf", required=False, type=str)
    return ap

def crop(frame, roi):
    tl, br = roi
    return frame[tl[1]:br[1], tl[0]:br[0]]


def main(args=None):

    if args is None:

        ap = get_parser()
        args = ap.parse_args()


    cap = cv2.VideoCapture(args.input)


    if args.roi:
        roi = args.roi.split("x")
        X = int(roi[0])
        rest = roi[1]
        Y, width, height = rest.split("+")

        Y = int(Y)
        width = int(width)
        height = int(height)
        ROI = ((X, Y), (X+width, Y+height))


    elif args.idtrackerai_conf:
        import json
        with open(args.idtrackerai_conf, "r") as fh:
            roi = json.load(fh)["_roi"]["value"]
        roi_cnt = np.array(eval(roi[0][0]))
        X, Y, width, height = cv2.boundingRect(roi_cnt)

        ROI = ((X, Y), (X+width, Y+height))
    else:
        ROI = ((0, 0), (cap.get(cv2.CAP_PROP_FRAME_WIDTH), cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))

    framerate = cap.get(cv2.CAP_PROP_FPS)
    nframes = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    pb = tqdm.tqdm(total=nframes, desc=f"Cropping ROI {ROI}  from frames")

    video_writer = cv2.VideoWriter(
        args.output,
        cv2.VideoWriter_fourcc(*"XVID"),
        framerate,
        (width, height)
    )

    ret = True
    while ret:
        ret, frame = cap.read()
        if not ret:
            break

        frame = crop(frame, ROI)
        video_writer.write(frame)
        pb.update(1)

    video_writer.release()
    cap.release()

if __name__ == "__main__":
    main()
