import argparse
from os import path

from cv2 import cv2
from tqdm import tqdm

from copycat.debugging.debugging import debug_params
from copycat.image_processing.note_press_detection import NoteDetector
from copycat.media_parsing.video_to_frames import Video
from copycat.notation.notation import Notation
from globals.global_types import Bounds, Clef
from globals.paino_key import PianoKey
from image_processing.key_extraction import get_piano_keys, automatically_detect_keyboard_line
from media_parsing.crop import crop_video
from media_parsing.skip_frames import skip_video_frames


def main(file_path: str, tempo: int, first_key: str, skip_frames: int, debug: bool):
    video = Video(file_path)
    frames = video.extract_frames()
    skip_video_frames(skip_frames, frames)

    control_frame = next(frames)

    detection_line_height = automatically_detect_keyboard_line(control_frame)

    if detection_line_height is None:
        if debug:
            cv2.imshow("unable to detect piano keyboard", control_frame)
            cv2.waitKey()
        raise Exception("Unable to detect piano keyboard")

    keys = get_piano_keys(control_frame, PianoKey.note_to_index(first_key), detection_line_height)
    detector = NoteDetector(control_frame, detection_line_height, 0.1)

    if debug:
        debug_params(control_frame, keys, detector)
        return

    n = Notation(fps=video.fps, tempo=tempo, octave_offset=-1, min_note_speed=1)
    try:
        for frame in tqdm(frames, desc="Parsing video"):
            for key in keys:
                clef = detector.is_note_detected(key.section, frame)
                if clef is not Clef.NONE:
                    n.push_note(key.note, clef=clef)
            n.apply_frame()
    except KeyboardInterrupt:
        print(n.get_abc_notation(title=path.basename(file_path), composer=""))
        raise


# Do not use unless necessary
def main_manual(
        file_path: str,
        bounds: Bounds,
        first_note: str,
        skip_frames: int,
        detector_line_offset: int,
        tempo: int,
        min_note_speed: int,
        debug: bool
):
    video = Video(file_path)
    frames = crop_video(video.extract_frames(), bounds)

    skip_video_frames(skip_frames, frames)

    control_frame = next(frames)

    keys = get_piano_keys(control_frame, PianoKey.note_to_index(first_note), detector_line_offset)
    detector = NoteDetector(control_frame, detector_line_offset, 0.1)

    if debug:
        debug_params(control_frame, frames, keys, detector, bounds)
        return

    n = Notation(fps=video.fps, tempo=tempo, octave_offset=-1, min_note_speed=min_note_speed)
    try:
        for frame in frames:
            for key in keys:
                clef = detector.is_note_detected(key.section, frame)
                if clef is not Clef.NONE:
                    n.push_note(key.note, clef=clef)
            n.apply_frame()
    except Exception:
        print(n.get_abc_notation(title=path.basename(file_path), composer=""))
        raise


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("-f", "--file", help="The path of the mp4 synthesia video", metavar="PATH", required=True)
    parser.add_argument("-k", "--first-key", help="The first white key in the bounds.", metavar="NOTE", default="A1")
    parser.add_argument("-t", "--tempo", help="The tempo of the piece in BPM", default=120, type=int)
    parser.add_argument("--skip-frames", help="How many frame to skip in case there is an introduction", default=0,
                        type=int)
    parser.add_argument("--debug", help="Show debugged version", default=False, action="store_true")

    subparsers = parser.add_subparsers(dest="command")

    manual = subparsers.add_parser("manual")
    manual.add_argument("--bounds", help="The boundaries around the piano keys space separated",
                        metavar="X Y WIDTH HEIGHT", required=False)
    manual.add_argument("--detector-line-offset",
                        help="Number of pixels from the top of the boundary to offset the detector line", type=int,
                        default=80)
    manual.add_argument("--min-speed", help="Defines a minimum note duration", type=int, default=2)

    args = parser.parse_args()

    if args.command == "manual":
        main_manual(file_path=args.file, bounds=Bounds(*[int(v) for v in args.bounds.split(" ")]),
                    first_note=args.first_key,
                    skip_frames=args.skip_frames, detector_line_offset=args.detector_line_offset,
                    tempo=args.tempo,
                    debug=args.debug, min_note_speed=args.min_speed)

    main(
        file_path=args.file,
        first_key=args.first_key,
        skip_frames=args.skip_frames,
        tempo=args.tempo,
        debug=args.debug
    )
