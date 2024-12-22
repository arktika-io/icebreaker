from icebreaker.store import Store
from icebreaker.store import KeyDoesNotExist
import pytest
from uuid import uuid4
from icebreaker.store import Read
from typing import Self


class TestRead:
    def test_does_not_crash(
        self: Self,
        populated_store: Store[Read],
        populated_store_key: str,
    ) -> None:
        if not populated_store.supports_read:
            pytest.skip("read not implemented")
        populated_store.read(key=populated_store_key)

    def test_does_not_crash_as_a_context_manager(
        self: Self,
        populated_store: Store[Read],
        populated_store_key: str,
    ) -> None:
        with populated_store.read(key=populated_store_key) as data:
            assert data.read()
        assert data.closed

    def test_raises_key_does_not_exist_when_attempting_to_read_non_existent_key(
        self: Self,
        populated_store: Store[Read],
    ) -> None:
        if not populated_store.supports_read:
            pytest.skip("read not implemented")

        with pytest.raises(KeyDoesNotExist):
            populated_store.read(key=str(uuid4()))
