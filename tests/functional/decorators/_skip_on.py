from functools import wraps
from typing import Any
from typing import Callable

import pytest


def skip_on(exception: type[BaseException], reason: str) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                return func(*args, **kwargs)
            except exception:
                pytest.skip(reason)

        return wrapper

    return decorator


skip_on_not_implemented_error = skip_on(
    exception=NotImplementedError,
    reason="The interfaces required for this test are not implemented.",
)
