from enum import StrEnum, auto


class Orientation(StrEnum):
  """Represents Orientations"""
  CLOCKWISE        = auto()
  COUNTERCLOCKWISE = auto()
  COLINEAR         = auto()
