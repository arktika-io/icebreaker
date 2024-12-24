from uuid import uuid4

import pytest

from icebreaker.store import Path
from icebreaker.store import Store
from icebreaker.store import StoreBackend
from icebreaker.store import Write


@pytest.fixture(scope="function")
def store(store_backend: StoreBackend) -> Store[StoreBackend]:
    return Store(store_backend=store_backend)


@pytest.fixture(scope="session")
def populated_store_path() -> Path:
    return Path(str(uuid4()))


@pytest.fixture(scope="function")
def populated_store(
    store: Store[Write],
    populated_store_path: Path,
) -> Store[StoreBackend]:
    try:
        store.write_string(path=populated_store_path, data="test")
    except NotImplementedError:
        pytest.skip("The interfaces required for this test are not implemented.")
    return store
