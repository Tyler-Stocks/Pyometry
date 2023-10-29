"""This error is raised when a line segment is invalid."""


class InvalidLineSegment(Exception):
  """Raised when a line segment is invalid."""

  def __init__(self, message: str) -> None:
    message = f"\b{message}\n"
    super().__init__(message)
