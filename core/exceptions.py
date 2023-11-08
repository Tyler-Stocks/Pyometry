class FormatError(Exception):
  """Raised when a string is formatted incorectly."""

  def __init__(self, *args: str, **kwargs: None) -> None:
    default_message: str = "Invalid Format In Constructor"

    if not args:
      args = default_message,

    super().__init__(*args, **kwargs)


class InvalidConstructor(Exception):
  """Raised when not enough constructor information is provided."""

  def __init__(self, *args: str, **kwargs: None) -> None:
    default_message: str = "Invalid Constructor"

    if not args:
      args = default_message,

    super().__init__(*args, **kwargs)

class InvalidLineSegment(Exception):
  """Raised when a line segment is invalid."""

  def __init__(self, *args: str, **kwargs: None) -> None:
    default_message: str = "The supplied line segment is not possible"

    if not args:
      args = default_message,

    super().__init__(*args, **kwargs)


class InvalidQuadrant(Exception):
  """This is an error for an invalid quadrant."""

  def __init__(self, *args: str, **kwargs: None) -> None:
    default_message: str = "The calculated quadrant does not exist"

    if not args:
      args = default_message,

    super().__init__(*args, **kwargs)


class InvalidVector(Exception):
  """Error raised when both the x and y componants of a vector are zero."""

  def __init__(self, *args: str, **kwargs: None) -> None:
    default_message: str = "Vector with componants (0,0) does not exist"

    if not args:
      args = default_message,

    super().__init__(*args, **kwargs)


class UnknownPrecision(Exception):
  """Raised when the precision in less than 1."""

  def __init__(self, *args: str, **kwargs: None) -> None:
    default_message: str = "Invalid supplied precision"

    if not args:
      args = default_message,

    super().__init__(*args, **kwargs)
