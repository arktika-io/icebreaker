from icebreaker.store_backends.protocol import Read
from icebreaker.store_backends.protocol import KeyDoesNotExist
import pytest
from uuid import uuid4


async def test_read_works(
    populated_store_backend: Read,
    populated_store_backend_key: str,
) -> None:
    await populated_store_backend.read(key=populated_store_backend_key)


async def test_read_raises_key_does_not_exist_when_attempting_to_read_non_existent_key(
    populated_store_backend: Read,
) -> None:
    with pytest.raises(KeyDoesNotExist):
        await populated_store_backend.read(key=str(uuid4()))
