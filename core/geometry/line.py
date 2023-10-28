# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------

from __future__ import annotations

# External Imports
from typing import Literal
from fractions import Fraction
from attrs import define

# Internal Imports
from core.geometry.point import Point2D
from core.util.undefined import Undefined
from core.errors.invalid_constructor import InvalidConstructor
from core.errors.format_error import FormatError


# -----------------------------------------------------------------------------
# Converter
# -----------------------------------------------------------------------------

@define
class _Line2DConverter:
  point_a: Point2D
  point_b: Point2D

  def to_string(self) -> str:
    """
    Convert a Line2D to a string.

    ### Return
    Returns a string representation of a line in the form:\n
    Point-A X: {value}, Point-B X: {value}\n
    Point-B X: {value}, Point-B X: {value}\n
    """
    return f"""Point-A X: {self.point_a.x}, Point-A Y: {self.point_a.y}
Point-B X: {self.point_b.x}, Point-B Y: {self.point_b.y}"""


  def to_list(self) -> list[Point2D]:
    """
    Converts a Line2D into a list of Point2D's

    ### Return
    Returns a list in the form [Point-A, Point-B]
    """
    return [self.point_a, self.point_b]


  def to_dict(self) -> dict[str, Point2D]:
    """
    Converts a Line2D into a dict of Point2D's

    ### Return
    Returns a dict in the form {"Point-A": [value], "Point-B" [value]}
    """

    return {"Point-A": self.point_a, "Point-B": self.point_b}

  def to_tuple(self) -> tuple[Point2D, Point2D]:
    """
    Converts a Line2D into a tuple of Point2D's

    ### Return
    Returns a tuple in the form (Point-A, Point-B)
    """

    return self.point_a, self.point_b


# -----------------------------------------------------------------------------
# Base Class
# -----------------------------------------------------------------------------


@define
class _Line2DProperties(_Line2DConverter):
  """_"""
  point_a: Point2D
  point_b: Point2D


  def __post_init__(self) -> None:
    super().__init__(self.point_a, self.point_b)


  def rise(
      self,
      return_type: Literal["Float"] | Literal["Fraction"]
    ) -> float | Fraction:
    """
    Returns the rise of the line.

    ### Parameters
     * return_type -> The type of return that you would like.

    ### Return
    Returns the vertical distance between two whole number points on the line.
    """
    rise: float = self.point_a.y - self.point_b.y

    match return_type:
      case "Float":
        return rise
      case "Fraction":
        return Fraction(rise)


  def run(
      self,
      return_type: Literal["Float"] | Literal["Fraction"]
    ) -> float | Fraction:
    """
    Returns the run of the line.

    ### Parameters

    * return_type => The return type you would like

    ### Return

    Returns the horizontal distance between two whole number points on the line
    """
    run: float = self.point_a.x_position - self.point_b.x_position

    match return_type:
      case "Float":
        return run
      case "Fraction":
        return Fraction(run)


  def slope(
      self,
      return_type: Literal["Fraction"] | Literal["Float"]
  ) -> Fraction | float | Undefined :
    """
    Returns the slope of the line.

    ### Parameters

    * return_type => defines the return type of the function either Fraction or Float.

    ### Returns

    Returns the steepness of the line
    """

    if self.run("Float") == 0:
      return Undefined.UNDEFINED

    slope: float | Fraction = self.rise("Float") / self.run("Float")

    match return_type:
      case "Fraction":
        return Fraction(slope)
      case "Float":
        return slope


  @property
  def x_intercept(self) -> Point2D:
    """Returns the point where the line crosses the x axis"""

    if not self.point_a.y:
      return self.point_a
    elif not self.point_b.y:
      return self.point_b

    slope: float | Undefined | Fraction = self.slope("Float")

    if slope is Undefined.UNDEFINED:
      return Point2D(self.point_a.x_position, 0)
    else:
      x_intercept_value: float = (
        self.point_b.x -
        (self.point_b.y / slope))

    return Point2D(x_intercept_value, 0)


  @property
  def y_intercept(self) -> Point2D:
    """Returns the point where the line crosses the y axis"""

    if self.point_a.x_position == 0:
      return self.point_a
    elif self.point_b.x_position == 0:
      return self.point_b

    slope: float | Undefined | Fraction = self.slope("Float")

    if slope is Undefined.UNDEFINED:
      return Point2D(self.point_a.x_position, 0)
    else:
      y_intercept_value: float = (
        self.point_b.y -
        (self.point_b.x / slope)
      )

    return Point2D(0, y_intercept_value)


# -----------------------------------------------------------------------------
# Constructor
# -----------------------------------------------------------------------------


@define
class _Line2DConstructor(_Line2DProperties):
  """ Should not be accessed."""
  point_a: Point2D
  point_b: Point2D

  def __post_init__(self) -> None:
    super().__init__(self.point_a, self.point_b)

  @classmethod
  def from_str(cls, points: str) -> _Line2DConstructor:
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
      raise InvalidConstructor(
        f"""
          Invalid amount of values provided in constructor. \n
          Excpected 2, got {length}
          """)

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
      raise InvalidConstructor(
        f"""
         Cannot construct point from x-value {first_point_values[0]}.\n
         X-Position must be a number.
         """)

    if not first_point_values[-1].isnumeric():
      raise InvalidConstructor(
        f"""
         Cannot construct point from y-value {first_point_values[-1]}.\n
         Y-Position must be a number.
         """)

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
      raise InvalidConstructor(
        f"""
         Cannot construct point from x-value {second_point_values[0]}.\n
         X-Position must be a number.
         """)

    if not second_point_values[-1].isnumeric():
      raise InvalidConstructor(
        f"""
         Cannot construct point from y-value {second_point_values[-1]}.\n
         Y-Position must be a number.
         """
      )

    start_point: Point2D = Point2D(
      float(first_point_values[0]),
      float(first_point_values[-1]))

    end_point: Point2D = Point2D(
      float(second_point_values[0]),
      float(second_point_values[-1])
    )

    return cls(start_point, end_point)


  @classmethod
  def from_dict(cls, points: dict[str, Point2D]) -> _Line2DConstructor:
    """
    Constructs a line from a dictionary.

    ### Parameters
    * point: A dictionary representing the Line in the form
      {"Point-A": Point2D, "Point-B": Point2D}
    """
    if not "Point-A" in points:
      raise InvalidConstructor(
        """
        Point-A was not found in the constructor.
        Please include Point-A to construct a line from a dict.
        """)

    if not "Point-B" in points:
      raise InvalidConstructor(
        """
        Point-B was not found in the constructor.
        Please include Point-B to construct a line from a dict.
        """)

    if points["Point-A"] == points["Point-B"]:
      raise InvalidConstructor(
        f"""
         To construct a Line2D two distinct points must be provided.
         Since {points['Point-A']} and {points['Point-B']} are not distinct
         the line could not be constructed
         """)

    return cls(points["Point-A"], points["Point-B"])


  @classmethod
  def from_tuple(cls, points: tuple[Point2D, Point2D]) -> _Line2DConstructor:
    """
    Constructs a Line2D from a tuple of Point2D

    ### Params
    * points => The points you would like to construct the line from.

    ### Note

    If you try to pass in two points with the same position the function will raise an error.
    """

    if points[0] == points[1]:
      raise InvalidConstructor(
        f"""
         To construct a Line2D two distinct points must be provided.
         Since {points[0]} and {points[1]} are not distinct the line could not be constructed
         """)

    return cls(points[0], points[1])


# -----------------------------------------------------------------------------
# Public Interface
# -----------------------------------------------------------------------------


@define
class Line2D(_Line2DConstructor):
  """Class representing a line projected in 2D space."""
  point_a: Point2D
  point_b: Point2D

  def __post_init__(self) -> None:
    return super().__init__(self.point_a, self.point_b)

  def is_perpendicular(self, other: Line2D) -> bool:
    """
    Returns whether or not two lines are perpendicular.

    Parameters
    ----------
    other: Line2D = The line that you are comparing against.
    """
    if not other.__class__ == Line2D:
      raise NotImplementedError(
        f"""
         Cannot perform comparison is_perpendicular on classes
         {self.__class__.__name__} and {other.__class__.__name__}.\n
         They are incompatible.
         """)

    if self.slope("Float") is Undefined and other.slope("Float") == 0:
      return True
    elif self.slope("Float") == 0 and other.slope("Float") is Undefined:
      return True
    else:
      is_perpendicular = (
        self.slope("Float") ==
        -1 / float(other.slope("Float")))
      return is_perpendicular


  def is_parallel(self, other: Line2D) -> bool:
    """
    Returns whether or not two lines are parallel.

    Parameters
    ----------
    other: Line2D = The line that you are comparing against.
    """
    if not other.__class__ == Line2D:
      raise NotImplementedError(
        f"""
         Cannot perform comparioson is_parallel on classes
         {self.__class__.__name__} and {other.__class__.__name__}.\n
         They are incompatible.
         """)

    return self.slope("Float") == other.slope("Float")
