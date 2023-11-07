# -------------------------------------------------------------------------------------------------
# Imports
# -------------------------------------------------------------------------------------------------

from __future__ import annotations

from dataclasses import dataclass

from core.geometry.point import Point2D


# -------------------------------------------------------------------------------------------------
# Converter
# -------------------------------------------------------------------------------------------------

@dataclass(order = True)
class _Ray2DConverter:
  start_point: Point2D
  direction:   float

  @staticmethod
  def to_tuple(ray: Ray2D) -> tuple[Point2D, float]:
    """
    Converts a Ray2D into a tuple in the form (Start-Point, direction)

    ### Paremeters
      * ray => The ray to be converted

    ### Return
      A tuple representation of the ray
    """
    return ray.start_point, ray.direction


  @staticmethod
  def to_dict(ray: Ray2D) -> dict[str, Point2D | float]:
    """
    Converts a Ray2D into a dict in the form {"Start-Point": [value], "Direction": [value]}

    ### Parameters
      * ray => The ray to be converted

    ### Return
      A dictionary representaion of the array
    """
    return {"Start-Point": ray.start_point, "Direction": ray.direction}


  @staticmethod
  def to_list(ray: Ray2D) -> list[Point2D | float]:
    """
    Converts a Ray2D into a list in the form [Start-Point, Direction]

    ### Parameters
      * ray => The ray to be converted

    ### Return
      A list representaion of the array
    """
    return [ray.start_point, ray.direction]


# -------------------------------------------------------------------------------------------------
# Constructer
# -------------------------------------------------------------------------------------------------


@dataclass(order = True)
class _Ray2DConstructer(_Ray2DConverter):
  """Internal Implementation Detail of Ray2D"""
  start_point: Point2D
  direction:   float


  @staticmethod
  def from_tuple(information: tuple[Point2D, float]) -> Ray2D:
    """
    Constructs a Ray2D from a tuple containing the end-point and direction

    ### Parameters
      * information => A tuple containing information about the tuple

    ### Return
      The constructed ray
    """
    return Ray2D(information[0], information[1])


  @staticmethod
  def from_dict(information: dict[str, float]) -> Ray2D:
    """
    Constructs a Ray2D from a dict containing the end-point and direction in the following form:
    {"Start-Point-X: [value], Start-Point-Y: [value], "distance": [value]}

    ### Parameters
      * information => A dict containing information about the ray

    ### Return
      The constructed ray
    """
    return Ray2D(
      Point2D(information["Start-Point-X"], information["Start-Point-Y"]), information["Direction"])


  @staticmethod
  def from_list(information: list[float]) -> Ray2D:
    """
    Constructs a Ray2D from a list containing its information in the following form:
    [Start Point X, Start Point Y, Direction]

    ### Parameters
      * information => The information about the Ray2D

    ###
      The constructed ray
    """
    return Ray2D(Point2D(information[0], information[1]), information[2])


  @staticmethod
  def from_str(information: str) -> Ray2D:
    """
    Constructs a Ray2D from a string in the following form:
    Start-Point X, Start-Point Y, direction

    ### Parameters
      * information => The information about the Ray

    ### Return
      The constructed ray
    """

    ray_information: list[str] = information.split(",")

    return Ray2D(
      Point2D(float(ray_information[0]), float(ray_information[1])), float(ray_information[2]))


# -------------------------------------------------------------------------------------------------
# Properties
# -------------------------------------------------------------------------------------------------




# -------------------------------------------------------------------------------------------------
# Public Interface
# -------------------------------------------------------------------------------------------------


@dataclass(order = True)
class Ray2D(_Ray2DConstructer):
  """Class Representing a two dimensional ray"""
  start_point: Point2D
  direction:   float


  