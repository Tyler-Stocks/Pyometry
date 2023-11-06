# -------------------------------------------------------------------------------------------------
# Imports
# -------------------------------------------------------------------------------------------------

from __future__ import annotations

# Standard Imports
from math import sqrt, pi, sin, cos
from typing import Literal
from fractions import Fraction
from dataclasses import dataclass

# Internal Imports
from core.util.quadrant import Quadrant
from core.util.angle_unit import AngleUnit
from core.util.orientation import Orientation
from core.exceptions import FormatError, InvalidConstructor


# -------------------------------------------------------------------------------------------------
# Converter
# -------------------------------------------------------------------------------------------------


@dataclass(order = True)
class _Point2DConverter:
  """Internal Implementation Detail of Point2D"""
  x: float
  y: float

  def to_tuple(self) -> tuple[float, float]:
    """
    Converts a Point2D into a tuple of floats

    ### Return
      The point as tuple in the form (x, y)
    """
    return self.x, self.y

  def to_dict(self) -> dict[str, float]:
    """
    Converts a Point2D into a dict of floats

    ### Return
      The point as a dict in the form {"x": {value}, "y": {value}}
    """
    return {"x": self.x, "y": self.y}


  def to_list(self) -> list[float]:
    """
    Converts a Point2D into a list of floats

    ### Return
      The point as a list in the form [x, y]
    """

    return [self.x, self.y]


# -------------------------------------------------------------------------------------------------
# Properties
# -------------------------------------------------------------------------------------------------


@dataclass(order = True)
class _PointProperties(_Point2DConverter):
  """Internal Implementation Detail of Point2D"""
  x: float
  y: float

  def __post_init__(self) -> None:
    return super().__init__(self.x, self.y)


  @property
  def quadrant(self) -> Quadrant:
    """
    Calculates the quadrant that the point is in

    ### Return
      The quadrant that the point is in
    """
    if not self.x and not self.y:
      return Quadrant.ORIGIN
    elif self.x > 0:
      return Quadrant.ONE if self.y > 0 else Quadrant.FOUR
    return Quadrant.TWO if self.y > 0 else Quadrant.THREE


  @property
  def distance_from_origin(self) -> float:
    """
    Calculates the distance from the point to the origin (0, 0)

    ### Return
      The distance between the point and the origin
    """
    return sqrt(self.x ** 2 + self.y ** 2)


  @property
  def is_at_origin(self) -> bool:
    """
    Calculates whether the point is at the origin (0,0)

    ### Return
      Whether or not the point is at the origin
    """
    return not self.x and not self.y


# --------------------------------------------------------------------------------------------------
# Constructor
# --------------------------------------------------------------------------------------------------


@dataclass(order = True)
class _Point2DConstructor(_PointProperties):
  """Internal Implementation Detail Of Point2D"""
  x: float
  y: float

  def __post_init__(self) -> None:
    return super().__init__(self.x, self.y)

  @classmethod
  def from_tuple(cls, position: tuple[float, float]) -> Point2D:
    """
    Constructs a point from a tuple of floats.

    ### Parameters
      * position => The position of the point (x,y).

    ### Return
      A Point2D constructed from the supplied tuple
    """
    return Point2D(position[0], position[1])


  @classmethod
  def from_str(cls, position: str) -> Point2D:
    """
    Constructs a point from a string in the for 'x,y'.

    ### Parameters
      * position => The position of the point 'x,y'

    ### Return
      A Point2D constructed from the supplied string
    """

    if not "," in position:
      raise FormatError(
        f"""
         Invalid string format for position argument.\n
         Must seperate values using , .
         {position} is not a valid parameter for position.
         """)

    position_list: list[str] = position.split(",")

    if not position_list[0].isnumeric():
      raise InvalidConstructor

    if not position_list[1].isnumeric():
      raise InvalidConstructor

    return Point2D(float(position_list[0]), float(position_list[1]))


  @classmethod
  def from_dict(cls, position: dict[str, float]) -> Point2D:
    """
    Constructs a point from a dictionary.

    ### Parameters
      * position => The position of the point {"x-position": value, "y-position": value}

    ### Return
      A Point2D constructed from the supplied dictionary
    """

    if not "x-position" in position:
      raise InvalidConstructor

    if not "y-position" in position:
      raise InvalidConstructor

    return Point2D(position["x-position"], position["y-position"])


  @classmethod
  def from_list(cls, position: list[float]) -> Point2D:
    """Constructs a Point2D from a List of floats"""
    return Point2D(position[0], position[1])


# --------------------------------------------------------------------------------------------------
# Public Interface
# --------------------------------------------------------------------------------------------------


@dataclass(order = True)
class Point2D(_Point2DConstructor):
  """Class Representing a Point2D"""
  x: float
  y: float

  def __post_init__(self) -> None:
    return super().__init__(self.x, self.y)

  def __eq__(self, other: object) -> bool:
    if not isinstance(other, Point2D):
      return False
    return self.x == other.x and self.y == other.y


  def __ne__(self, other: object) -> bool:
    if not isinstance(other, Point2D):
      return True
    return not self.x == other.x and self.y == other.y


  def translate_point(self, translation_x: float, translation_y: float) -> None:
    """
    Translates the point on both axises based on input.

    ### Parameters
      * translation_x => The distance to translate x.
      * translation_y => The distance to translate y.
    """

    self.x += translation_x
    self.y += translation_y


  def get_vertical_distance(
    self,
    other: Point2D,
    return_type: Literal["Float"] | Literal["Fraction"] = "Float"
  ) -> float | Fraction:
    """
    Returns the vertical distance between two points.

    ### Parameters
      * other => The point you are trying to find the distance to.
      * return_type => The return type of the function

    ### Return
      The vertical distance between self and other.
    """

    v_dist: float = self.x - other.x

    if return_type == "Fraction":
      return Fraction(v_dist)

    return v_dist


  def get_horizontal_distance(
    self,
    other: Point2D,
    return_type: Literal["Float"] | Literal["Fraction"] = "Float"
  ) -> float | Fraction:
    """
    Returns the horizontal distance between two points.

    ### Parameters
      * other => The point you are getting the distance too.
      * return_type => The return type of the function

    ### Return
      The horizontal distance between self and other
    """
    h_dist: float = self.y - other.y

    if return_type == "Fraction":
      return Fraction(h_dist)

    return h_dist


  def get_distance_between_points(self, other: Point2D) -> float:
    """
    Calculates the distance between two points.

    ### Parameters
      * other => The point you are getting the distance too.

    ### Return
      Returns the distance between self and other
    """
    return sqrt(self.get_horizontal_distance(other) ** 2 + self.get_vertical_distance(other) ** 2)


  def mirror_x_axis(self) -> None:
    """Mirrors the point across to the X axis."""
    self.x *= -1


  def mirror_y_axis(self) -> None:
    """Mirrors the point across to the Y axis."""
    self.y *= -1


  def rotate_about_origin(
      self,
      angle_of_rot: float,
      angle_unit:   AngleUnit,
      direction:    Orientation,
  ) -> None:
    """
    Rotates the point about the origin.

    ### Params
      * angle_of_rot => The angle about the origin that you are rotating.
      * angle_type   => The angle unit (DEG/RAD).
      * direction    => The direction of rotation.
    """
    if angle_unit is AngleUnit.RAD:
      angle_of_rot *= (pi / 180)
    cos_theta: float = cos(angle_of_rot)
    sin_theta: float = sin(angle_of_rot)

    if direction is Orientation.CLOCKWISE:
      self.x = -(self.x * cos_theta + self.y * sin_theta)
      self.y = -(self.x * sin_theta + self.y * cos_theta)
    elif direction is Orientation.COUNTERCLOCKWISE:
      self.x = self.x * cos_theta - self.y * sin_theta
      self.y = self.x * sin_theta + self.y * cos_theta



  def rotate_point(
      self,
      other:        Point2D,
      angle_of_rot: float,
      angle_unit:   AngleUnit,
      direction:    Orientation
  ) -> None:
    """
    Rotates a point about another point.

    ### Parameters
      * other => The point you are rotating about.
      * angle_of_rot => The angle of rotation about the other point.
      * angle_type => The angle unit (Deg/Rad)
      * direction => The direction of rotation.
    """
    if angle_unit is AngleUnit.RAD:
      angle_of_rot *= (180 / pi)
    cos_theta: float = cos(angle_of_rot)
    sin_theta: float = sin(angle_of_rot)

    translated_x_position = self.x - other.x
    translated_y_position = self.y - other.y

    if direction is Orientation.CLOCKWISE:
      self.x = (
        translated_x_position
        * cos_theta
        + translated_y_position
        * sin_theta
      )
      self.y = (
        translated_y_position
        * sin_theta
        + translated_y_position
        * cos_theta
      )
    elif direction is Orientation.COUNTERCLOCKWISE:
      self.x = (
        translated_x_position
        * cos_theta
        - translated_y_position
        * sin_theta
      )
      self.y = (
        translated_y_position
        * sin_theta
        - translated_y_position
        * sin_theta
      )


  @staticmethod
  def get_orientation(
    point_1: Point2D,
    point_2: Point2D,
    point_3: Point2D
  ) -> Orientation:
    """
    Gets the orientation of three points.

    ### Parameters
      * point_1 => The first point
      * point_2 => The second point
      * point_3 => The third point

    ### Return
      The orientation of the points
    """
    orientation = (
      ((point_2.y - point_1.y) * (point_3.x - point_2.x)) -
      ((point_2.x - point_1.x) * (point_3.y - point_2.y))
      )

    if orientation > 0:
      return Orientation.CLOCKWISE
    elif orientation < 0:
      return Orientation.COUNTERCLOCKWISE

    return Orientation.COLINEAR
