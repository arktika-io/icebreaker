from uuid import uuid4

import pytest

from icebreaker.store import Store
from icebreaker.store import StoreBackend
from icebreaker.store import Write


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
    try:
        store.write_string(key=populated_store_key, data="test")
    except NotImplementedError:
        pytest.skip("The interfaces required for this test are not implemented.")
    return store
