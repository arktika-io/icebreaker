from uuid import uuid4

import pytest

from icebreaker.store import Append
from icebreaker.store import Delete
from icebreaker.store import Read
from icebreaker.store import Store
from icebreaker.store import Write
from icebreaker.store import WriteIfNotExists


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
