from bisect import bisect_left
from typing import Type, List

T = Type["T"]


def take_closest(thing_list: List[T], thing: T):
    """
    Assumes thing_list is sorted. Returns the index of the closest value to thing.

    If two numbers are equally close, return the largest number index.

    Based on:
        https://stackoverflow.com/questions/12141150/from-list-of-integers-get-number-closest-to-a-given-value
    """
    pos = bisect_left(thing_list, thing)
    if pos == 0:
        return 0
    if pos == len(thing_list):
        return len(thing_list) - 1
    before = thing_list[pos - 1]
    after = thing_list[pos]
    if after - thing <= thing - before:
        return pos
    else:
        return pos - 1