from icebreaker.store import Store
from icebreaker.store import KeyDoesNotExist
import pytest
from uuid import uuid4
from icebreaker.store import Read
from icebreaker.store import Delete
from typing import Self


class TestDelete:
    def test_does_not_crash(
        self: Self,
        populated_store: Store[Read],
        populated_store_key: str,
    ) -> None:
        if not isinstance(populated_store._store_backend, Delete):
            pytest.skip("delete not implemented")
        populated_store.delete(key=populated_store_key)

    def test_raises_key_does_not_exist_when_attempting_to_delete_non_existent_key(
        self: Self,
        populated_store: Store[Read],
    ) -> None:
        if not isinstance(populated_store._store_backend, Delete):
            pytest.skip("delete not implemented")
        with pytest.raises(KeyDoesNotExist):
            populated_store.delete(key=str(uuid4()))
