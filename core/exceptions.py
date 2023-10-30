class FormatError(Exception):
  """Raised when a string is formatted incorectly."""

  def __init__(self, message: str) -> None:
    super().__init__(message)


class InvalidConstructor(Exception):
  """Raised when not enough constructor information is provided."""

  def __init__(self) -> None:
    super().__init__("Not enought information was provided to construct the object.")


class InvalidLineSegment(Exception):
  """Raised when a line segment is invalid."""

  def __init__(self) -> None:
    super().__init__("The constructed line segment is not possible.")


class InvalidQuadrantError(Exception):
  """This is an error for an invalid quadrant."""

  def __init__(self) -> None:
    super().__init__("The calculated quadrant does not exist.")


class InvalidVector(Exception):
  """Error raised when both the x and y componants of a vector are zero."""

  def __init__(self):
    super().__init__("A vector where x and y are zero is not possible.")


class UnknownPrecision(Exception):
  """Raised when the precision in less than 1."""

  def __init__(self) -> None:
    super().__init__("The precision that was supplied is not possible. Precision must be >= 1")
