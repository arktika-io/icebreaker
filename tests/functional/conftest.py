import pytest

from tests.functional.fixtures.memory_store_backend import *
from pytest import FixtureRequest
from icebreaker.store_backends.protocol import Read
from uuid import uuid4
from io import BytesIO


@pytest.fixture(scope="session")
def populated_store_backend_key() -> str:
    return str(uuid4())


@pytest.fixture(scope="session")
def populated_store_backend_data() -> bytes:
    return b"fake"


@pytest.fixture(scope="function", params=["memory_store_backend"])
async def populated_store_backend(
    request: FixtureRequest,
    populated_store_backend_key: str,
    populated_store_backend_data: bytes,
) -> Read:
    store_backend = request.getfixturevalue(request.param)
    await store_backend.write(key=populated_store_backend_key, data=BytesIO(populated_store_backend_data))
    return store_backend
