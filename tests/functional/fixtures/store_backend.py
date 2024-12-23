import pytest
from pytest import FixtureRequest

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
