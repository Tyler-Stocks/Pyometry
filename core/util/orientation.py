from enum import StrEnum, auto


class Orientation(StrEnum):
  """Represents different possible orientations"""
  CLOCKWISE        = auto()
  COUNTERCLOCKWISE = auto()
  COLINEAR         = auto()
