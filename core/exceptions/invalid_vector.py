"""Exception for invalid vector."""


class InvalidVector(Exception):
  """Error raised when both the x and y componants of a vector are zero."""

  def __init__(self, message: str):
    self.message = f"\b{message}\n"
    super().__init__(message)
