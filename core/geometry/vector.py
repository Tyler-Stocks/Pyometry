# -------------------------------------------------------------------------------------------------
# Imports
# -------------------------------------------------------------------------------------------------


# Future
from __future__ import annotations

# Standard
from math import pi, sqrt, atan, cos, sin
from dataclasses import dataclass

# Internal
from core.util.quadrant import Quadrant
from core.util.angle_unit import AngleUnit
from core.exceptions import InvalidVector, FormatError, InvalidConstructor


# --------------------------------------------------------------------------------------------------
# Converter
# --------------------------------------------------------------------------------------------------


@dataclass
class _Vector2DConverter:
  x: float
  y: float


  def to_str(self) -> str:
    """
    Converts a Vector2D into a string

    ### Return
      A string in the form {x: [value], y: [value]}
    """
    return f"x: {self.x}, y: {self.y}"


  def to_tuple(self) -> tuple[float, float]:
    """
    Converts a Vector2D into a tuple of floats

    ### Return
      A tuple in the form (x, y)
    """
    return self.x, self.y

  def to_dict(self) -> dict[str, float]:
    """
    Converts a Vector2D into a tuple of floats

    ### Return
      A dict in the form {"x": {value}, "y": {value}}
    """
    return {"x-component": self.x, "y-component": self.y}

  def to_list(self) -> list[float]:
    """
    Converts a Vector2D into a list of floats

    ### Return
      A list in the form [x, y]
    """
    return [self.x, self.y]


# -------------------------------------------------------------------------------------------------
# Properties
# -------------------------------------------------------------------------------------------------


@dataclass
class _Vector2DProperties(_Vector2DConverter):
  x: float
  y: float

  def __post_init__(self) -> None:
    return super().__init__(self.x, self.y)

  @property
  def quadrant(self) -> Quadrant:
    """
    Calculates the quadrant of the vector.

    ### Return
      The quadrant the vector is in
    """
    if not self.x or not self.y:
      return Quadrant.NONE

    if self.x > 0:
      return Quadrant.ONE if self.y > 0 else Quadrant.FOUR
    return Quadrant.TWO if self.y > 0 else Quadrant.THREE


  @property
  def direction(self) -> float:
    """
    Calculates the direction of the vector.

    ### Return
      The direction of the vector
    """

    if not self.x and self.y < 0:
      direction = 90.00
    elif not self.x and self.y > 0:
      direction = -90.00
    elif not self.y and self.x < 0:
      direction = 90.00
    elif not self.y and self.x > 0:
      direction = -90.00

    direction = atan(self.x / self.y)

    if self.quadrant in (Quadrant.TWO, Quadrant.THREE):
      direction += 180
    elif self.quadrant is Quadrant.FOUR:
      direction += 360
    return direction


  @property
  def magnitude(self) -> float:
    """
    Calculates the magnitude of the vector.

    ### Return
      The magnitude of the vector
    """
    return sqrt(self.x ** 2 + self.y ** 2)


# -------------------------------------------------------------------------------------------------
# Constructor
# -------------------------------------------------------------------------------------------------


@dataclass
class _Vector2DConstructor(_Vector2DProperties):
  x: float
  y: float

  def __post_init__(self) -> None:
    return super().__init__(self.x, self.y)

  @classmethod
  def from_tuple(cls, componants: tuple[float, float]) -> Vector2D:
    """
    Constructs a vector from a tuple.

    ### Parameters
      * componants => The x and y componants of the vector in form (x-componant, y_componant)

    ### Return
      A Vector2D constructed from the supplied tuple
    """

    return Vector2D(componants[0], componants[1])


  @classmethod
  def from_str(cls, componants: str) -> Vector2D:
    """
    Constructs a vector from a string.

    ### Parameters
      * componants => The componants in the form "x-componant,y-componant"

    ### Return
      A Vector2D constructed form the supplied string
    """

    if not "," in componants:
      raise FormatError(
        f"""
         Invalid string format for position argument.\n
         Must seperate values using , .
         {componants} is not a valid parameter for position.
         """
      )

    componants_list: list[str] = componants.split(",")

    length: int = len(componants_list)

    if not length == 2:
      raise InvalidConstructor

    if not componants_list[0].isnumeric():
      raise InvalidConstructor

    if not componants_list[1].isnumeric():
      raise InvalidConstructor

    return Vector2D(float(componants_list[0]), float(componants_list[1]))


  @classmethod
  def from_dict(cls, componants: dict[str, float]) -> Vector2D:
    """
    Constructs Vector2D from a dictionary.

    ### Parameters
      * componants = The componants of the vector {"x-componant": value, "y-componant": value}

    ### Return
      A Vector2D constructed from the supplied dictionary
    """

    if not "x-componant" in componants:
      raise InvalidConstructor

    if not "y-componant" in componants:
      raise InvalidConstructor

    return Vector2D(componants["x-componant"], componants["y-componant"])


# -------------------------------------------------------------------------------------------------
# Public Interface
# -------------------------------------------------------------------------------------------------


@dataclass
class Vector2D(_Vector2DConstructor):
  """Class representing a two dimensional vector"""
  x: float
  y: float


  def __post_init__(self) -> None:
    if not self.x and not self.y:
      raise InvalidVector

    return super().__init__(self.x, self.y)


  def __add__(self, other: Vector2D) -> Vector2D:
    return Vector2D(self.x + other.x, self.y + other.y)


  def __radd__(self, other: Vector2D) -> Vector2D:
    return self + other


  def __sub__(self, other: Vector2D) -> Vector2D:
    return Vector2D(self.x - other.x, self.y - other.y)


  def __rsub__(self, other: Vector2D) -> Vector2D:
    return other - self


  def __mul__(self, scalar: float) -> Vector2D:
    return Vector2D(self.x * scalar, self.y * scalar)


  def __rmul__(self, scalar: float) -> Vector2D:
    return self * scalar


  def __truediv__(self, scalar: float) -> Vector2D:
    if not scalar:
      raise ValueError("Cannot scale a vector by zero. (Cannot divide by zero)")
    return Vector2D(self.x / scalar, self.y / scalar)


  def __rtruediv__(self, scalar: float) -> Vector2D:
    return scalar / self


  def rotate(self, rotation: float, angle_type: AngleUnit) -> None:
    """
    Rotates the vector around the origin.

    ### Parameters
      * rotation   => The angle of rotation
      * angle_unit => The angle unit to use (DEG/RAD)
    """

    if angle_type is AngleUnit.RAD:
      rotation = rotation * (180 / pi)

    self.x = (
        cos(rotation * self.x)
        - sin(rotation * self.y)
    )
    self.y = (
        sin(rotation * self.x)
        + cos(rotation * self.y)
    )
