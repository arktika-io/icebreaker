from uuid import uuid4

import pytest
from pytest import FixtureRequest

from icebreaker.store import Store
from icebreaker.store_backends.protocol import Append
from icebreaker.store_backends.protocol import Delete
from icebreaker.store_backends.protocol import Read
from icebreaker.store_backends.protocol import StoreBackend
from icebreaker.store_backends.protocol import Write
from icebreaker.store_backends.protocol import WriteIfNotExists


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


@pytest.fixture(
    scope="function",
    params=[
        "memory_store_backend",
        "env_vars_store_backend",
        "env_var_store_backend",
    ],
)
def store_backend_implementing_append(request: FixtureRequest) -> Append:
    store_backend: Append = request.getfixturevalue(request.param)
    return store_backend


@pytest.fixture(
    scope="function",
    params=[
        "memory_store_backend",
        "env_vars_store_backend",
        "env_var_store_backend",
    ],
)
def store_backend_implementing_delete(request: FixtureRequest) -> Delete:
    store_backend: Delete = request.getfixturevalue(request.param)
    return store_backend


@pytest.fixture(
    scope="function",
    params=[
        "memory_store_backend",
        "env_vars_store_backend",
        "env_var_store_backend",
    ],
)
def store_backend_implementing_read(request: FixtureRequest) -> Read:
    store_backend: Read = request.getfixturevalue(request.param)
    return store_backend


@pytest.fixture(
    scope="function",
    params=[
        "memory_store_backend",
        "env_vars_store_backend",
        "env_var_store_backend",
    ],
)
def store_backend_implementing_write(request: FixtureRequest) -> Write:
    store_backend: Write = request.getfixturevalue(request.param)
    return store_backend


@pytest.fixture(
    scope="function",
    params=[
        "memory_store_backend",
        "env_vars_store_backend",
        "env_var_store_backend",
    ],
)
def store_backend_implementing_write_if_not_exists(request: FixtureRequest) -> WriteIfNotExists:
    store_backend: WriteIfNotExists = request.getfixturevalue(request.param)
    return store_backend


@pytest.fixture(scope="function")
def store_implementing_append(store_backend_implementing_append: Append) -> Store[Append]:
    return Store(store_backend=store_backend_implementing_append)


@pytest.fixture(scope="function")
def store_implementing_delete(store_backend_implementing_delete: Delete) -> Store[Delete]:
    return Store(store_backend=store_backend_implementing_delete)


@pytest.fixture(scope="function")
def store_implementing_read(store_backend_implementing_read: Read) -> Store[Read]:
    return Store(store_backend=store_backend_implementing_read)


@pytest.fixture(scope="function")
def store_implementing_write(store_backend_implementing_write: Write) -> Store[Write]:
    return Store(store_backend=store_backend_implementing_write)


@pytest.fixture(scope="function")
def store_implementing_write_if_not_exists(
    store_backend_implementing_write_if_not_exists: WriteIfNotExists,
) -> Store[WriteIfNotExists]:
    return Store(store_backend=store_backend_implementing_write_if_not_exists)


@pytest.fixture(scope="session")
def populated_store_key() -> str:
    return str(uuid4())


@pytest.fixture(scope="function")
def populated_store_implementing_read(
    store_implementing_write: Store[Write],
    populated_store_key: str,
) -> Store[Read]:
    store_implementing_write.write_string(key=populated_store_key, data="test")
    return store_implementing_write


@pytest.fixture(scope="function")
def populated_store_implementing_delete(
    store_implementing_delete: Store[Delete],
    populated_store_key: str,
) -> Store[Delete]:
    store_implementing_delete.write_string(key=populated_store_key, data="test")
    return store_implementing_delete


@pytest.fixture(scope="function")
def populated_store_implementing_write_if_not_exists(
    store_implementing_write_if_not_exists: Store[WriteIfNotExists],
    populated_store_key: str,
) -> Store[WriteIfNotExists]:
    store_implementing_write_if_not_exists.write_string(key=populated_store_key, data="test")
    return store_implementing_write_if_not_exists
