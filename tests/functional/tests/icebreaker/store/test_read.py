from icebreaker.store import Store
from icebreaker.store import KeyDoesNotExist
import pytest
from uuid import uuid4


async def test_read_works(
    populated_store: Store,
    populated_store_key: str,
) -> None:
    if not populated_store.supports_read:
        pytest.skip(f"read not implemented")
    await populated_store.read(key=populated_store_key)


async def test_read_raises_key_does_not_exist_when_attempting_to_read_non_existent_key(
    populated_store: Store,
) -> None:
    if not populated_store.supports_read:
        pytest.skip(f"read not implemented")

    with pytest.raises(KeyDoesNotExist):
        await populated_store.read(key=str(uuid4()))
