"""Raised when not enough constructor information is provided."""


class InvalidConstructor(Exception):
  """Raised when not enough constructor information is provided."""

  def __init__(self, message: str) -> None:
    super().__init__(message)
