import argparse
import os.path
import math
import tqdm
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("--video", type=str)
ap.add_argument("--nframes", type=int, default=math.inf)
args = ap.parse_args()

def read_and_write(cap, vw):

    ret, frame = cap.read()
    if not ret:
        return 1, None
    if vw is None:
        path = os.path.dirname(args.video)
        filename = os.path.basename(args.video)
        filename, extension = args.video.split(".")
        output_filename = os.path.join(path, filename + "_safe" + "." + extension)
        vw = cv2.VideoWriter(output_filename, cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame.shape[1], frame.shape[0]))
    vw.write(frame)
    return 0, vw


def main():
    
    cap = cv2.VideoCapture(args.video)
    vw = None
    
    nframes = min(cap.get(cv2.CAP_PROP_FRAME_COUNT), args.nframes)
    print(f"Reading video with {nframes} frames")
    pbar = tqdm.tqdm(total=nframes)
    count = 0

    for _ in tqdm.tqdm(range(nframes)):
         status, vw = read_and_write(cap, vw)
         if status != 0:
             break
         else:
             count += 1
      
    
    if count != nframes:
        print("W: I have not processed all the frames I was supposed to")
    
    cap.release()
    if vw is None:
        vw.release()

if __name__ == "__main__":
    main()
