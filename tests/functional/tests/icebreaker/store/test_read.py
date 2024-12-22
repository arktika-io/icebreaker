from icebreaker.store import Store
from icebreaker.store import KeyDoesNotExist
import pytest
from uuid import uuid4
from icebreaker.store import Read


def test_read_works(
    populated_store: Store[Read],
    populated_store_key: str,
) -> None:
    if not populated_store.supports_read:
        pytest.skip("read not implemented")
    populated_store.read(key=populated_store_key)


def test_read_raises_key_does_not_exist_when_attempting_to_read_non_existent_key(
    populated_store: Store[Read],
) -> None:
    if not populated_store.supports_read:
        pytest.skip("read not implemented")

    with pytest.raises(KeyDoesNotExist):
        populated_store.read(key=str(uuid4()))
