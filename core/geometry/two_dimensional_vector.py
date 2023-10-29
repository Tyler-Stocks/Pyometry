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
from core.exceptions.invalid_vector import InvalidVector
from core.exceptions.format_error import FormatError
from core.exceptions.invalid_constructor import InvalidConstructor


# --------------------------------------------------------------------------------------------------
# Converter
# --------------------------------------------------------------------------------------------------


@dataclass
class _Vector2DConverter:
  x_componant: float
  y_componant: float


  def to_str(self) -> str:
    """
    Converts a Vector2D into a string

    ### Return
      Returns a string in the form "x-componant: {value}, y-componant: {value}"
    """
    return f"x-componant: {self.x_componant}, y-componant: {self.y_componant}"


  def to_tuple(self) -> tuple[float, float]:
    """
    Converts a Vector2D into a tuple of floats

    ### Return
      Returns a tuple in the form (x-component, y-component)
    """
    return self.x_componant, self.y_componant

  def to_dict(self) -> dict[str, float]:
    """
    Converts a Vector2D into a tuple of floats

    ### Return
      Returns a dict in the form {"x-component": {value}, "y-component": {value}}
    """
    return {"x-component": self.x_componant, "y-component": self.y_componant}

  def to_list(self) -> list[float]:
    """
    Converts a Vector2D into a list of floats

    ### Return
      Returns a list in the form [x-component, y-component]
    """
    return [self.x_componant, self.y_componant]


# -------------------------------------------------------------------------------------------------
# Properties
# -------------------------------------------------------------------------------------------------


@dataclass
class _Vector2DProperties(_Vector2DConverter):
  x_componant: float
  y_componant: float

  def __post_init__(self) -> None:
    return super().__init__(self.x_componant, self.y_componant)

  @property
  def quadrant(self) -> Quadrant:
    """
    Calculates the quadrant of the vector.

    ### Return
      Returns the quadrant that the vector is in.
    """
    if not self.x_componant or not self.y_componant:
      return Quadrant.NONE

    if self.x_componant > 0:
      return Quadrant.ONE if self.y_componant > 0 else Quadrant.FOUR
    return Quadrant.TWO if self.y_componant > 0 else Quadrant.THREE


  @property
  def direction(self) -> float:
    """
    Calculates the direction of the vector.

    ### Return
      Returns the direction of the vector
    """

    if not self.x_componant and self.y_componant < 0:
      direction = 90.00
    elif not self.x_componant and self.y_componant > 0:
      direction = -90.00
    elif not self.y_componant and self.x_componant < 0:
      direction = 90.00
    elif not self.y_componant and self.x_componant > 0:
      direction = -90.00

    direction = atan(self.x_componant / self.y_componant)

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
      Returns the magnitue of the vector
    """
    return sqrt(self.x_componant ** 2 + self.y_componant ** 2)


# -------------------------------------------------------------------------------------------------
# Constructor
# -------------------------------------------------------------------------------------------------


@dataclass
class _Vector2DConstructor(_Vector2DProperties):
  x_componant: float
  y_componant: float

  def __post_init__(self) -> None:
    return super().__init__(self.x_componant, self.y_componant)

  @classmethod
  def from_tuple(cls, componants: tuple[float, float]) -> Vector2D:
    """
    Constructs a vector from a tuple.

    ### Parameters
      * componants => The x and y componants of the vector in form (x-componant, y_componant)
    """

    return Vector2D(componants[0], componants[1])


  @classmethod
  def from_str(cls, componants: str) -> Vector2D:
    """
    Constructs a vector from a string.

    ### Parameters
      * componants => The componants in the form "x-componant,y-componant"
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
      raise InvalidConstructor(
        f"""
         Two many values in constructor call. \n
         Excpected 2 values, got {length}.
         """)

    if not componants_list[0].isnumeric():
      raise InvalidConstructor(
        f"""
         Cannot construct point from x componant {componants_list[0]}.
         X componant must be a number.
         """
      )

    if not componants_list[1].isnumeric():
      raise InvalidConstructor(
        f"""
         Cannot construct vector from y componant {componants_list[1]}.
         """)

    return Vector2D(float(componants_list[0]), float(componants_list[1]))


  @classmethod
  def from_dict(cls, componants: dict[str, float]) -> Vector2D:
    """
    Constructs Vector2D from a dictionary.

    ###Parameters
      * componants = The componants of the vector {"x-componant": value, "y-componant": value}
    """

    if not "x-componant" in componants:
      raise InvalidConstructor(
        f"""
         Canot find value for x-componant. \n
         Excpected 'x-componant' at position [0],
         got {list(componants)[0]}
         """)

    if not "y-componant" in componants:
      raise InvalidConstructor(
        f"""
         Cannot find value for y-componant. \n
         Excpected 'y-componant' at position [-1],
         got {list(componants)[-1]}
         """)

    return Vector2D(componants["x-componant"], componants["y-componant"])


# -------------------------------------------------------------------------------------------------
# Public Interface
# -------------------------------------------------------------------------------------------------


@dataclass
class Vector2D(_Vector2DConstructor):
  """Class representing a two dimensional vector"""
  x_componant: float
  y_componant: float


  def __post_init__(self) -> None:
    if not self.x_componant and not self.y_componant:
      raise InvalidVector("Vector (0,0) does not exist.")

    return super().__init__(self.x_componant, self.y_componant)


  def __add__(
    self,
    addend: Vector2D
  ) -> Vector2D:
    if not addend.__class__ is Vector2D:
      raise NotImplementedError(
          f"""
           Cannot perform operation __add__ on {type(addend)}
           """)

    sum_of_x_componants: float = self.x_componant + addend.x_componant
    sum_of_y_componants: float = self.y_componant + addend.y_componant
    return Vector2D(sum_of_x_componants, sum_of_y_componants)


  def __radd__(
      self,
      addend: Vector2D
  ) -> Vector2D:
    return self + addend


  def __sub__(
    self,
    subtrahend: Vector2D
  ) -> Vector2D:
    if not subtrahend.__class__ is Vector2D:
      raise NotImplementedError(
        f"""
          Cannot perform operation __sub__ on {type(subtrahend)}
          """)
    sum_of_x_componants: float = self.x_componant + subtrahend.x_componant
    sum_of_y_componants: float = self.y_componant + subtrahend.y_componant
    return Vector2D(sum_of_x_componants, sum_of_y_componants)


  def __rsub__(
      self,
      subtrahend: Vector2D
  ) -> Vector2D:
    return subtrahend - self


  def __mul__(
      self,
      scalar: float
  ) -> Vector2D:
    if not scalar.__class__ == float:
      raise NotImplementedError(
        f"""Cannot perform operation __mul__ on {type(scalar)}
         """)
    prod_of_x_componants: float = self.x_componant * scalar
    prod_of_y_componants: float = self.y_componant * scalar
    return Vector2D(prod_of_x_componants, prod_of_y_componants)


  def __rmul__(
      self,
      scalar: float
  ) -> Vector2D:
    return self * scalar


  def __truediv__(
      self,
      scalar: float
    ) -> Vector2D:
    if not scalar.__class__ == float:
      raise NotImplementedError(
        f"""
         Cannot perform operation __div__ on {type(scalar)}
         """)
    div_of_x_componants: float = self.x_componant / scalar
    div_of_y_componants: float = self.y_componant / scalar
    return Vector2D(div_of_x_componants, div_of_y_componants)


  def __rtruediv__(
      self,
      scalar: float
  ) -> Vector2D:
    return scalar / self


  def rotate(self, rotation: float, angle_type: AngleUnit) -> None:
    """
    Rotates the vector around the origin.

    Parameters
    ----------
    rotation: float = The angle of rotation
    angle_unit: AngleUnit = The angle unit to use (DEG/RAD)
    Description
    -----------
    Rotatest the vector around the origin through the following formula:
      x componant = cos(rotation * x componant) - sin(rotation * y componant) \n
      y componant = sin(rotation * x componant) - cos(rotation * y componant)
    """

    if angle_type is AngleUnit.RAD:
      rotation = rotation * (180 / pi)

    self.x_componant = (
        cos(rotation * self.x_componant)
        - sin(rotation * self.y_componant)
    )
    self.y_componant = (
        sin(rotation * self.x_componant)
        + cos(rotation * self.y_componant)
    )
