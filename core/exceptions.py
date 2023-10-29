class FormatError(Exception):
  """Raised when a string is formatted incorectly."""

  def __init__(self, message: str) -> None:
    message = f"\b{message}\n"

    super().__init__(message)


class InvalidConstructor(Exception):
  """Raised when not enough constructor information is provided."""

  def __init__(self, message: str) -> None:
    super().__init__(message)


class InvalidLineSegment(Exception):
  """Raised when a line segment is invalid."""

  def __init__(self, message: str) -> None:
    message = f"\b{message}\n"
    super().__init__(message)


class InvalidQuadrantError(Exception):
  """This is an error for an invalid quadrant."""

  def __init__(self, message: str) -> None:
    message = f"\b{message}\n"
    super().__init__(message)


class InvalidVector(Exception):
  """Error raised when both the x and y componants of a vector are zero."""

  def __init__(self, message: str):
    self.message = f"\b{message}\n"
    super().__init__(message)


class UnknownPrecision(Exception):
  """Raised when the precision in less than 1."""

  def __init__(self, message: str) -> None:
    message = f"\b{message}\n"
    super().__init__(message)
