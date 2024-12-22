import pytest

from tests.functional.fixtures.memory_store_backend import *  # noqa
from tests.functional.fixtures.env_vars_store_backend import *  # noqa
from tests.functional.fixtures.env_var_store_backend import *  # noqa
from pytest import FixtureRequest
from icebreaker.store_backends.protocol import Write
from icebreaker.store_backends.protocol import StoreBackend
from uuid import uuid4
from icebreaker.store import Store


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


@pytest.fixture(scope="function")
def store(store_backend: StoreBackend) -> Store[StoreBackend]:
    return Store(store_backend=store_backend)


@pytest.fixture(scope="session")
def populated_store_key() -> str:
    return str(uuid4())


@pytest.fixture(scope="function")
def populated_store(
    store: Store[Write],
    populated_store_key: str,
) -> Store[StoreBackend]:
    store.write_string(key=populated_store_key, data="test")
    return store
