import argparse
import os.path

from idtrackerai.postprocessing.individual_videos import generate_individual_videos
from idtrackerai.postprocessing.trajectories_to_video import generate_trajectories_video
from idtrackerai_app.win_idtrackerai import get_video_object_and_trajectories


def get_parser():

    ap = argparse.ArgumentParser()
    ap.add_argument("--video", dest="video_path", required=True)
    ap.add_argument("--session-folder", dest="session", required=True)
    return ap


def main(args=None):

    if args is None:
        parser = get_parser()
        args = parser.parse_args()

    session = os.path.basename(args.session.strip("/"))

    video_object, trajectories = get_video_object_and_trajectories(
        args.video_path, session
    )

    generate_individual_videos(video_object, trajectories, label="identity")
    generate_trajectories_video(video_object, trajectories)


if __name__ == "__main__":
    main()
