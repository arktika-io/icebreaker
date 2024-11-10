import pytest

from tests.functional.fixtures.memory_store_backend import *
from tests.functional.fixtures.env_vars_store_backend import *

from tests.functional.fixtures.env_var_store_backend import *
from pytest import FixtureRequest
from icebreaker.store_backends.protocol import Read
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
def store_backend(request: FixtureRequest) -> Read:
    return request.getfixturevalue(request.param)


@pytest.fixture(scope="function")
def store(store_backend: Read) -> Read:
    return Store(store_backend=store_backend)


@pytest.fixture(scope="session")
def populated_store_key() -> str:
    return str(uuid4())


@pytest.fixture(scope="function")
async def populated_store(
    store: Store,
    populated_store_key: str,
) -> Read:
    await store.write_string(key=populated_store_key, data="test")
    return store
