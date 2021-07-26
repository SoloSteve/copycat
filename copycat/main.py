import argparse

from global_types import Bounds
from media_parsing.video_to_frames import extract_frames
from processing.key_extraction import get_piano_keys
from processing.note_press_detection import NoteDetector
from processing.paino_key import PianoKey


def main(file_path: str, bounds: Bounds, first_note: str, skip_frames):
    frames = extract_frames(file_path)
    for i in range(skip_frames):
        next(frames)

    control_frame = next(frames)
    keys = get_piano_keys(control_frame, bounds, PianoKey.note_to_index(first_note))
    detector = NoteDetector(control_frame, bounds.y + 80, 0.2)
    for frame in frames:
        pressed = []
        for key in keys.values():
            if detector.is_note_detected(key.contour, frame):
                pressed.append(key.note)
        print(f"{pressed}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    manual = parser.add_subparsers().add_parser("manual")
    manual.add_argument("--file", help="The path of the mp4 synthesia video", metavar="PATH", required=True)
    manual.add_argument("--bounds", help="The boundaries around the piano keys space separated",
                        metavar="X Y WIDTH HEIGHT", required=True)
    manual.add_argument("--first-key", help="The first white key in the bounds.", metavar="NOTE", required=True)
    manual.add_argument("--skip-frames", help="How many frame to skip in case there is an introduction", default=0,
                        type=int)
    args = parser.parse_args()
    main(args.file, Bounds(*[int(v) for v in args.bounds.split(" ")]), args.first_key, args.skip_frames)
