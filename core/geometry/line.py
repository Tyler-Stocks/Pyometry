# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------

from __future__ import annotations

# Standard Imports
from typing import Literal
from fractions import Fraction
from dataclasses import dataclass

# Internal Imports
from core.geometry.point import Point2D
from core.geometry.line_segment import LineSegment2D
from core.util.undefined import Undefined
from core.exceptions import InvalidConstructor, FormatError


# -----------------------------------------------------------------------------
# Converter
# -----------------------------------------------------------------------------

@dataclass(order = True)
class _Line2DConverter:
  point_a: Point2D
  point_b: Point2D


  def to_list(self) -> list[Point2D]:
    """
    Converts a Line2D into a list of Point2D's

    ### Return
      A list in the form [Point-A, Point-B]
    """
    return [self.point_a, self.point_b]


  def to_dict(self) -> dict[str, Point2D]:
    """
    Converts a Line2D into a dict of Point2D's

    ### Return
      A dict in the form {"Point-A": [value], "Point-B" [value]}
    """

    return {"Point-A": self.point_a, "Point-B": self.point_b}

  def to_tuple(self) -> tuple[Point2D, Point2D]:
    """
    Converts a Line2D into a tuple of Point2D's

    ### Return
      A tuple in the form (Point-A, Point-B)
    """

    return self.point_a, self.point_b


# -----------------------------------------------------------------------------
# Base Class
# -----------------------------------------------------------------------------


@dataclass(order = True)
class _Line2DProperties(_Line2DConverter):
  """_"""
  point_a: Point2D
  point_b: Point2D


  def rise(self, return_type: Literal["Float"] | Literal["Fraction"]) -> float | Fraction:
    """
    Returns the rise of the line.

    ### Parameters
     * return_type -> The type of return that you would like.

    ### Return
      The vertical distance between two whole number points on the line.
    """
    rise: float = self.point_a.y - self.point_b.y

    if return_type == "Float":
      return rise
    return Fraction(rise)


  def run(self, return_type: Literal["Float"] | Literal["Fraction"]) -> float | Fraction:
    """
    Returns the run of the line.

    ### Parameters
      * return_type => The return type you would like

    ### Return
      The horizontal distance between two whole number points on the line
    """
    run: float = self.point_a.x - self.point_b.x

    match return_type:
      case "Float":
        return run
      case "Fraction":
        return Fraction(run)


  def slope(
    self,
    return_type: Literal["Fraction"] | Literal["Float"] = "Float"
  ) -> Fraction | float | Undefined :
    """
    Calculates the slope of the

    ### Parameters
      * return_type => defines the return type of the function either Fraction or Float.

    ### Returns
      The steepness of the line
    """

    if self.run("Float") == 0:
      return Undefined()

    slope: float | Fraction = self.rise("Float") / self.run("Float")

    match return_type:
      case "Fraction":
        return Fraction(slope)
      case "Float":
        return slope


  @property
  def x_intercept(self) -> Point2D:
    """
    Calculates the point where the line crosses the x-axis

    ### Return
      The point where the line crosses the x-axis (0, {intercept})
    """

    if not self.point_a.y:
      return self.point_a
    elif not self.point_b.y:
      return self.point_b
    else:
      slope: float | Undefined | Fraction = self.slope("Float")

      if slope is Undefined:
        return Point2D(self.point_a.x, 0)
      else:
        x_intercept_value: float | Undefined = self.point_b.x - (self.point_b.y / slope)

      return Point2D(float(x_intercept_value), 0)


  @property
  def y_intercept(self) -> Point2D:
    """
    Calculates the point where the line crosses the y-axis

    ### Return
      The point where the line crosses the y-axis({intercept}, 0)
    """

    if not self.point_a.x:
      return self.point_a
    elif not self.point_b.x:
      return self.point_b
    else:
      slope: float | Undefined | Fraction = self.slope("Float")

      if slope is Undefined:
        return Point2D(self.point_a.x, 0)
      else:
        y_intercept_value: float | Undefined = (
          self.point_b.y -
          (self.point_b.x / slope)
        )

      return Point2D(0, float(y_intercept_value))




# -----------------------------------------------------------------------------
# Constructor
# -----------------------------------------------------------------------------


@dataclass(order = True)
class _Line2DConstructor(_Line2DProperties):
  """Internal Implementation Detail of Line2D"""
  point_a: Point2D
  point_b: Point2D


  @classmethod
  def from_str(cls, points: str) -> Line2D:
    """
    Constructs a line segment 2D from a str.

    ### Parameters
      * points => A string representation of a line in the form x:y,x:y
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
         """)

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
      float(second_point_values[-1]))

    return Line2D(start_point, end_point)


  @classmethod
  def from_dict(cls, points: dict[str, Point2D]) -> Line2D:
    """
    Constructs a line from a dictionary.

    ### Parameters
      * point => A dictionary representing the Line in the form
        {"Point-A": Point2D, "Point-B": Point2D}
    """
    if not "Point-A" in points or not "Point-B" in points:
      raise InvalidConstructor

    if points["Point-A"] == points["Point-B"]:
      raise InvalidConstructor

    return Line2D(points["Point-A"], points["Point-B"])


  @classmethod
  def from_tuple(cls, points: tuple[Point2D, Point2D]) -> Line2D:
    """
    Constructs a Line2D from a tuple of Point2D

    ### Params
      * points => The points you would like to construct the line from.

    ### Note
      If you try to pass in two points with the same position the function will raise an error.
    """

    if points[0] == points[1]:
      raise InvalidConstructor

    return Line2D(points[0], points[1])


# -----------------------------------------------------------------------------
# Public Interface
# -----------------------------------------------------------------------------


@dataclass(order = True)
class Line2D(_Line2DConstructor):
  """Class representing a line projected in 2D space."""
  point_a: Point2D
  point_b: Point2D


  def is_perpendicular(self, other: Line2D) -> bool:
    """
    Returns whether or not two lines are perpendicular.

    ### Parameters
      * other => The line that you are comparing against.
    """

    if self.slope() is Undefined and not other.slope():
      return True
    elif not self.slope() and other.slope() is Undefined:
      return True
    else:
      is_perpendicular = self.slope() == -1 / float(other.slope())
      return is_perpendicular


  def is_parallel(self, other: Line2D | LineSegment2D) -> bool:
    """
    Returns whether or not two lines are parallel.

    ### Parameters
      * other => The line that you are comparing against.
    """

    return self.slope() == other.slope()
