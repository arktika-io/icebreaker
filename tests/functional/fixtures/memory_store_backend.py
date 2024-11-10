import pytest

from icebreaker.store_backends.memory import MemoryStoreBackend


@pytest.fixture(scope="function")
def memory_store_backend() -> MemoryStoreBackend:
    return MemoryStoreBackend()
