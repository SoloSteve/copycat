import pytest

from copycat.globals.paino_key import PianoKey
from globals.global_types import Section

temp = Section(0, 0)


@pytest.mark.parametrize(
    "test_index,expected_note",
    [
        (0, "A1"), (1, "A#1"), (2, "B1"), (3, "C1"),
        (12, "A2"), (17, "D2")
    ]
)
def test_key_construction(test_index: int, expected_note: str):
    assert PianoKey(test_index, section=temp).note == expected_note


@pytest.mark.parametrize(
    "test_note,expected_index",
    [
        ("A1", 0), ("A#1", 1), ("B1", 2), ("C1", 3),
        ("A2", 12), ("D2", 17)
    ]
)
def test_note_to_index(test_note: str, expected_index: int):
    assert PianoKey.note_to_index(test_note) == expected_index
