from typing import NamedTuple
from enum import Enum


class Orientation(Enum):
    NORTH = 0,
    WEST = 1,
    SOUTH = 2,
    EAST = 3

ORIENTATION_DECODE = ["NORTE", "OESTE", "SUR", "ESTE"]

class Point(NamedTuple):
    x: int
    y: int

class EvalFlags:
    POSITION = 1
    ORIENTATION = 2
    BEEPERBAG = 4
    ALLBEEPERS = 8

class WallFlags:
    UP = 1
    LEFT = 2
    DOWN = 4
    RIGHT = 8
    ALL = 15
    

