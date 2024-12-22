from icebreaker.store import Store
import pytest
from uuid import uuid4
from icebreaker.store import Read
from icebreaker.store import Delete
from typing import Self


class TestDeleteIfExists:
    def test_does_not_crash(
        self: Self,
        populated_store: Store[Read],
        populated_store_key: str,
    ) -> None:
        if not isinstance(populated_store._store_backend, Delete):
            pytest.skip("delete_if_exists not implemented")
        populated_store.delete_if_exists(key=populated_store_key)

    def test_does_not_raise_when_attempting_to_delete_non_existent_key(
        self: Self,
        populated_store: Store[Read],
    ) -> None:
        if not isinstance(populated_store._store_backend, Delete):
            pytest.skip("delete_if_exists not implemented")
        populated_store.delete_if_exists(key=str(uuid4()))
