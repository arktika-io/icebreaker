import pytest
from pytest import FixtureRequest

from icebreaker.store_backends.protocol import StoreBackend


@pytest.fixture(
    scope="function",
    params=[
        "memory_store_backend",
        "env_vars_store_backend",
        "env_var_store_backend",
    ],
)
def store_backend(request: FixtureRequest) -> StoreBackend:
    store_backend: StoreBackend = request.getfixturevalue(request.param)
    return store_backend
