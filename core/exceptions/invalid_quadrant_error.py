"""This is an error for an invalid quadrant."""


class InvalidQuadrantError(Exception):
  """This is an error for an invalid quadrant."""

  def __init__(self, message: str) -> None:
    message = f"\b{message}\n"
    super().__init__(message)
