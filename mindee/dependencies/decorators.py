import functools
from collections.abc import Callable
from typing import ParamSpec, TypeVar

from mindee.dependencies.checkers import require_pillow, require_pypdfium2

P = ParamSpec("P")
R = TypeVar("R")


def requires_pillow(func: Callable[P, R]) -> Callable[P, R]:
    """Decorator to enforce Pillow availability on a function/method."""

    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        require_pillow()
        return func(*args, **kwargs)

    return wrapper


def requires_pypdfium2(func: Callable[P, R]) -> Callable[P, R]:
    """Decorator to enforce PyPDFium2 availability on a function/method."""

    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        require_pypdfium2()
        return func(*args, **kwargs)

    return wrapper
