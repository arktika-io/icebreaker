from typing import Self
from uuid import uuid4

from icebreaker.store import Delete
from icebreaker.store import Store


class TestDeleteIfExists:
    def test_does_not_crash(
        self: Self,
        populated_store_implementing_delete: Store[Delete],
        populated_store_key: str,
    ) -> None:
        populated_store_implementing_delete.delete_if_exists(key=populated_store_key)

    def test_does_not_raise_when_attempting_to_delete_non_existent_key(
        self: Self,
        store_implementing_delete: Store[Delete],
    ) -> None:
        store_implementing_delete.delete_if_exists(key=str(uuid4()))
