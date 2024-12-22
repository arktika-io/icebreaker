from typing import Self
from uuid import uuid4

import pytest

from icebreaker.store import Delete
from icebreaker.store import KeyDoesNotExist
from icebreaker.store import Store


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
