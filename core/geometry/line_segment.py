# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------

# Future
from __future__ import annotations

# Standard
from typing import Literal, SupportsIndex
from fractions import Fraction
from math import sqrt
from dataclasses import dataclass

# Internal
from core.geometry.point import Point2D
from core.geometry.line  import Line2D
from core.util.undefined import Undefined
from core.util.orientation import Orientation
from core.exceptions import InvalidLineSegment, FormatError, InvalidConstructor


# -----------------------------------------------------------------------------
# Converter
# -----------------------------------------------------------------------------


@dataclass(order = True)
class _LineSegment2DConverter:
  """Internal Implementation detail of LineSegment2D"""
  start_point: Point2D
  end_point:   Point2D


  def to_tuple(self) -> tuple[Point2D, Point2D]:
    """
    Converts a line segment into a tuple of points

    ### Return
      A tuple in the form (Start Point, End Point)
    """
    return self.start_point, self.end_point


  def to_dict(self) -> dict[str, Point2D]:
    """
    Converts a line segment into a dict.

    ### Return
      A dict in the form {Start Point: {value}, End Point: {value}}
    """
    return {"Start Point": self.start_point, "End Point": self.end_point}


  def to_list(self) -> list[Point2D]:
    """
    Converts a line segment into a list.

    ### Return
      A list in the form [Start Point, End Point]
    """
    return [self.start_point, self.end_point]


# -----------------------------------------------------------------------------
# Properties
# -----------------------------------------------------------------------------


@dataclass(order = True)
class _LineSegment2DProperties(_LineSegment2DConverter):
  """Internal Implementation detail of LineSegment2D"""
  start_point: Point2D
  end_point:   Point2D

  def __post_init__(self) -> None:
    return super().__init__(self.start_point, self.end_point)


  @property
  def center(self) -> Point2D:
    """
    Calculates the center of the line segment.

    ### Return
      Returns the point at the center of the line segment
    """
    return Point2D(float(self.run(precision=5)) / 2, float(self.rise(prescision=5) / 2))


  def run(
      self,
      return_type: Literal["Float"] | Literal["Fraction"] = "Float",
      precision: SupportsIndex = 0
  ) -> float | Fraction:
    """
    Calculates the run (horizontal distance) of the line segment

    ### Parameters
      * return_type => Defines the return type of the function

    ### Return
      The horizontal distance between whole number points on the line segment.
    """
    run: float | Fraction = round((self.start_point.x - self.end_point.x) ** 2, precision)

    if return_type == "Fraction":
      return Fraction(run)
    return run


  def rise(
      self,
      return_type: Literal["Float"] | Literal["Fraction"] = "Float",
      prescision: SupportsIndex = 0
  ) -> float | Fraction:
    """
    Calculates the rise (vertical distance) of the line segment

    ### Parameters
      * return_type => Defines the return type of the function

    ### Return
      The vertical distance between whole number points on the line segment
    """
    rise: float | Fraction = round((self.start_point.y - self.end_point.y) ** 2, prescision)

    if return_type == "Fraction":
      return Fraction(rise)
    return rise


  def length(self, precision: SupportsIndex = 5) -> float:
    """
    Calculates the length of the line segment

    ### Parameters
      * precision => How precise you would like the calculation to be.

    ### Return
      The length of the line segment
    """
    return sqrt(self.run(precision=precision) ** 2 + self.rise(prescision=precision) ** 2)


  def slope(
      self,
      return_type: Literal["Float"] | Literal["Fraction"] = "Float",
      precision: SupportsIndex = 3
    ) -> float | Undefined | Fraction:
    """
    Calculates the slope of a line segment

    ### Parameters
      * return_type => The return type you would like, defaults to a decimal
      * precision   => How precise you would like the calculation to be

    ### Return
      The slope of the line
    """

    if not self.run():
      return Undefined()

    slope: float | Fraction = self.rise(prescision=precision) / self.run(precision=precision)

    if return_type == "Fraction":
      return Fraction(slope)
    return slope


# -----------------------------------------------------------------------------
# Constructor
# -----------------------------------------------------------------------------


@dataclass(order = True)
class _LineSegment2DConstructor(_LineSegment2DProperties):
  """Internal Implementation Detail Of LineSegment2D"""
  start_point: Point2D
  end_point: Point2D

  def __post_init__(self) -> None:
    super().__init__(self.start_point, self.end_point)


  @classmethod
  def from_tuple(cls, points: tuple[Point2D, Point2D]) -> LineSegment2D:
    """
    Constructs a line from a tuple of point.

    ### Parameters
      * points => The start and end point of a line segment (start_point, end_point)

    ### Return
      A LineSegment2D constructed from the supplied tuple
    """

    return LineSegment2D(points[0], points[1])


  @classmethod
  def from_str(cls, points: str) -> LineSegment2D:
    """
    Constructs a line from a string.

    ### Parameters
      * points => The start and end points of a line segment in the form:
        "start_point(x:y),end-point(x:y)"

    ### Return
      A LineSegment2D constructed from a supplied string
    """


    points_list: list[str] = points.split(",")

    length: int = len(points_list)


    if not "," in points:
      raise FormatError(
        f"""
         Invalid string format for points argument. \n
         Must seperate values using ",". \n
         {points} is not a valid format.
         """)


    if not length == 2:
      raise InvalidConstructor

    first_point: str = points_list[0]


    if not ":" in first_point:
      raise FormatError(
        f"""
         Invalid string format for start_point.\n
         Excpected "x-position:y-position",
         got {first_point}.
         """
      )

    first_point_values: list[str] = first_point.split(":")

    if not first_point_values[0].isnumeric():
      raise InvalidConstructor
    if not first_point_values[-1].isnumeric():
      raise InvalidConstructor

    second_point: str = points_list[1]

    if not ":" in second_point:
      raise FormatError(
        f"""
         Invalid string format for end_point.\n
         Excpected "x-position:y-position",
         got {second_point}.
         """)

    second_point_values: list[str] = second_point.split(":")

    if not second_point_values[0].isnumeric():
      raise InvalidConstructor

    if not second_point_values[-1].isnumeric():
      raise InvalidConstructor

    start_point: Point2D = Point2D(
      float(first_point_values[0]),
      float(first_point_values[-1]))

    end_point: Point2D = Point2D(
      float(second_point_values[0]),
      float(second_point_values[-1])
    )

    if start_point == end_point:
      raise InvalidConstructor

    return LineSegment2D(start_point, end_point)


  @classmethod
  def from_dict(cls, points: dict[str, Point2D]) -> LineSegment2D:
    """
    Constructs a line from a dictionary.

    ### Parameters
      * points => The start and end points of the line segment
        {"start_point": Point2D, "end_point}: "Point2D

    ### Return
      A LineSegment2D constructed from the supplied dictionary
    """

    if not "start_point" in points:
      raise InvalidConstructor

    if not "end-point" in points:
      raise InvalidConstructor

    if points["start-point"] == points["end-point"]:
      raise InvalidConstructor

    return LineSegment2D(points["start-point"], points["end-point"])


  @classmethod
  def from_list(cls, points: list[Point2D]) -> LineSegment2D:
    """
    Constructs a line segment from a list.

    ### Parameters
      * points => The points you would like to convert into a line

    ### Return
      A LineSegment2D constructed from the supplied list
    """

    if points[0] == points[1]:
      raise InvalidConstructor

    return LineSegment2D(points[0], points[1])


# -----------------------------------------------------------------------------
# Public Interface
# -----------------------------------------------------------------------------


@dataclass(order = True)
class LineSegment2D(_LineSegment2DConstructor):
  """Class representing a Line Segment in 2D space."""
  start_point: Point2D
  end_point: Point2D

  def __post_init__(self) -> None:
    if self.start_point == self.end_point:
      raise InvalidLineSegment

    return super().__init__(self.start_point, self.end_point)


  def is_between(self, point: Point2D) -> bool:
    """
    Checks if a point is along the line segment.

    ### Parameters
      point => The point you are checking is along a line.

    ### Return
      Whether or not a point in on the line segment
    """

    return bool(
      point.get_distance_between_points(self.start_point)
      + point.get_distance_between_points(self.end_point)
      == self.length()
      )


  def translate_x(self, translation: float) -> None:
    """
    Translates the line along the x axis.

    ### Parameters
    translation => The distance to translate the line segment.
    """

    self.start_point.x += translation
    self.end_point.x   += translation


  def translate_y(self, translation: float) -> None:
    """
    Translates the line along the y axis.

    ### Parameters
    translation => The distance to translate the line segment.
    """

    self.start_point.y += translation
    self.end_point.y   += translation


  def translate(self, x_translation: float, y_translation: float) -> None:
    """
    Translates the line by the given distances.

    ### Parameters
    x_translation => The distance to translate horizontally.
    y_translation => The distance to translate vertically.
    """

    self.translate_x(x_translation)
    self.translate_y(y_translation)


  def mirror_x(self) -> None:
    """Mirrors the line segment across the x-axis."""
    self.start_point.mirror_x_axis()
    self.end_point.mirror_x_axis()


  def mirror_y(self) -> None:
    """Mirrors the line segment acrossthe y-axis."""
    self.start_point.mirror_y_axis()
    self.end_point.mirror_y_axis()


  def is_parallel(self, line: LineSegment2D | Line2D) -> bool:
    """
    Checks to see if a line segment is parallel.

    ### Parameters
      * line => The line to be checked

    ### Return
      Whether or not the lines are parallel
    """
    return self.slope("Float") == line.slope("Float")


  def is_perpendicular(self, line: LineSegment2D | Line2D) -> bool:
    """
    Checks to see if a line segment is perpendicular

    ### Parameters
      * line => The line to be checked
    """
    if not self.slope("Float") is Undefined or line.slope("Float") is Undefined:
      return self.slope("Float") == 1 / line.slope("Float")

    if self.slope("Float") is Undefined and line.slope("Float") is Undefined:
      return False
    return True


  def intersects(self, line_segment: LineSegment2D) -> bool:
    """
    Checks whether or not two line segments intersects.

    ### Parameters
      * line_segment => The line segment you would like to check

    ### Return
      Whether or not the line segments intersect
    """

    orientation_1: Orientation = Point2D.get_orientation(
      self.start_point,
      self.end_point,
      line_segment.start_point)

    orientation_2: Orientation = Point2D.get_orientation(
      self.start_point,
      self.end_point,
      line_segment.end_point)

    orientation_3: Orientation = Point2D.get_orientation(
      line_segment.start_point,
      line_segment.end_point,
      self.start_point)

    orientation_4: Orientation = Point2D.get_orientation(
      line_segment.start_point,
      line_segment.end_point,
      self.end_point)

    if ((orientation_1 != orientation_2) and(orientation_3 != orientation_4)):
      return True

    if (
      orientation_1 is Orientation.COLINEAR and
      LineSegment2D.on_segment(self, line_segment.start_point)
    ):
      return True

    if (
      orientation_1 is Orientation.COLINEAR and
      LineSegment2D.on_segment(self, line_segment.end_point)
    ):
      return True

    if (
      orientation_1 is Orientation.COLINEAR and
      LineSegment2D.on_segment(line_segment, self.end_point)
    ):
      return True

    if (
      orientation_1 is Orientation.COLINEAR and
      LineSegment2D.on_segment(line_segment, self.end_point)
    ):
      return True

    return False


  @staticmethod
  def on_segment(segment: LineSegment2D, point: Point2D) -> bool:
    """
    Checks whether or not a point is on a line segment.

    ### Parameters
      * segment => The segment to check if the point is on
      * point   => The point to check if is on the segment

    ### Return
      Whether or not the supplied point is on the supplied line segment
    """
    if (
      (point.x <= max(segment.start_point.x, segment.end_point.x)) and
      (point.x >= min(segment.start_point.x, segment.end_point.x)) and
      (point.y <= max(segment.start_point.y, segment.end_point.y)) and
      (point.y >= min(segment.start_point.y, segment.end_point.y))
    ):
      return True
    return False
