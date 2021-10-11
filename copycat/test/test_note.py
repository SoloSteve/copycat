import pytest

from notation.note_parser import NoteParser


@pytest.mark.parametrize(
    "frame_count,tempo,expected_beat_count",
    [
        (30, 60, 1), (60, 60, 2), (15, 120, 1), (7, 120, 0.47)
    ]
)
def test_beat_count(frame_count: int, tempo: int, expected_beat_count: int):
    assert NoteParser.get_beat_count(frame_count, 30, tempo) == expected_beat_count


@pytest.mark.parametrize(
    "beat_count,expected_beat_length",
    [
        (1, 1), (0.23, 0.25), (0.08, 0.0625)
    ]
)
def test_beat_length(beat_count: float, expected_beat_length: float):
    assert NoteParser.round_beat_length(beat_count) == expected_beat_length
