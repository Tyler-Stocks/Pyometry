"""Class representing a format error."""


class FormatError(Exception):
  """Raised when a string is formatted incorectly."""

  def __init__(self, message: str) -> None:
    message = f"\b{message}\n"

    super().__init__(message)
