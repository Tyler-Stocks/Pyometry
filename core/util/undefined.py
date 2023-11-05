from __future__ import annotations

from typing import Any, Literal

class Undefined:
  """Represents undefined."""


  def __float__(self) -> float:
    return 0


  def __add__(self, _: Any) -> Undefined:
    return Undefined()


  def __sub__(self, _: Any) -> Undefined:
    return Undefined()


  def __mul__(self, _: Any) -> Undefined:
    return Undefined()


  def __truediv__(self, _: Any) -> Undefined:
    return Undefined()


  def __radd__(self, _: Any) -> Undefined:
    return Undefined()


  def __rsub__(self, _: Any) -> Undefined:
    return Undefined()


  def __rmul__(self, _: Any) -> Undefined:
    return Undefined()


  def __rtruediv__(self, _: Any) -> Undefined:
    return Undefined()


  def __eq__(self, _: Any) -> Literal[False]:
    return False


  def __ne__(self, _: Any) -> Literal[True]:
    return True
