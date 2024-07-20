import argparse

import cv2
from webcolors import hex_to_rgb

from debugging.debugging import debug_params
from image_processing.note_press_detection import NoteDetector
from media_parsing.video_to_frames import Video
from notation.notation import Notation
from globallll.color import Color
from globallll.global_types import Clef
from globallll.piano_key import PianoKey
from image_processing.key_extraction import get_piano_keys, automatically_detect_keyboard_line
from media_parsing.skip_frames import skip_video_frames
from notation.note_stream import get_note_stream


def main(
        file_path: str,
        tempo: int,
        first_key: str,
        skip_seconds: float,
        debug: bool,
        treble_color: str,
        bass_color: str
):
    video = Video(file_path)
    frames = video.extract_frames(25)
    skip_video_frames(round(skip_seconds * video.fps), frames)

    control_frame = next(frames)

    treble_color = Color.from_rgb(*hex_to_rgb(treble_color))
    bass_color = Color.from_rgb(*hex_to_rgb(bass_color))

    detection_line_height = automatically_detect_keyboard_line(control_frame)

    if detection_line_height is None:
        if debug:
            cv2.imshow("unable to detect piano keyboard", control_frame)
            cv2.waitKey()
        raise Exception("Unable to detect piano keyboard")

    keys = get_piano_keys(control_frame, PianoKey.note_to_index(first_key), detection_line_height)
    detector = NoteDetector(control_frame, detection_line_height, 0.1, treble_color, bass_color)

    if debug:
        debug_params(control_frame, keys, detector)
        return

    note_stream = get_note_stream(frames, video.total_frames, keys, detector, Clef.TREBLE)
    notation = Notation(video.fps, tempo, 0)
    notation_string = notation.parse_stream(note_stream)
    print(notation.get_abc_notation(notation_string))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("-f", "--file", help="The path of the mp4 synthesia video", metavar="PATH", required=True)
    parser.add_argument("-k", "--first-key", help="The first white key in the bounds.", metavar="NOTE", default="A1")
    parser.add_argument("-t", "--tempo", help="The tempo of the piece in BPM", default=120, type=int)
    parser.add_argument("-s", "--skip", help="How many seconds to skip in case there is an introduction", default=0,
                        type=float)
    parser.add_argument("--debug", help="Show debugged version", default=False, action="store_true")

    parser.add_argument("-tc","--treble-color", help="The (approximate) color of the pressed key for treble clef",
                        default="#00FF00", type=str)
    parser.add_argument("-bc","--bass-color", help="The (approximate) color of the pressed key for bass clef",
                        default="#0000FF", type=str)

    args = parser.parse_args()
    
    main(
        file_path=args.file,
        first_key=args.first_key,
        skip_seconds=args.skip,
        tempo=args.tempo,
        debug=args.debug,
        treble_color=args.treble_color,
        bass_color=args.bass_color,
    )