from icebreaker.store import Store
from icebreaker.store import KeyDoesNotExist
import pytest
from uuid import uuid4
from icebreaker.store import Delete
from typing import Self


class TestDelete:
    def test_does_not_crash(
        self: Self,
        populated_store_implementing_delete: Store[Delete],
        populated_store_key: str,
    ) -> None:
        populated_store_implementing_delete.delete(key=populated_store_key)

    def test_raises_key_does_not_exist_when_attempting_to_delete_non_existent_key(
        self: Self,
        store_implementing_delete: Store[Delete],
    ) -> None:
        with pytest.raises(KeyDoesNotExist):
            store_implementing_delete.delete(key=str(uuid4()))
