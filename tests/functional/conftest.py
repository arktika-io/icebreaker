import pytest

from tests.functional.fixtures.memory_store_backend import *
from tests.functional.fixtures.env_vars_store_backend import *

from tests.functional.fixtures.env_var_store_backend import *
from pytest import FixtureRequest
from icebreaker.store_backends.protocol import Read
from uuid import uuid4
from io import BytesIO
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


@pytest.fixture(scope="session")
def populated_store_data() -> bytes:
    return b"fake"


@pytest.fixture(scope="function")
async def populated_store(
    store: Store,
    populated_store_key: str,
    populated_store_data: bytes,
) -> Read:
    await store.write(key=populated_store_key, data=BytesIO(populated_store_data))
    return store
