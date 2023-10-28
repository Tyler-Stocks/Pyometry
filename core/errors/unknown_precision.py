"""Exception that is raised when the precision is less than 1."""


class UnknownPrecision(Exception):
  """Raised when the precision in less than 1."""

  def __init__(self, message: str) -> None:
    message = f"\b{message}\n"
    super().__init__(message)
