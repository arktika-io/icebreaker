from typing import Self
from uuid import uuid4

from icebreaker.store import Delete
from icebreaker.store import Store
from tests.functional.decorators import skip_on_not_implemented_error


class TestDeleteIfExists:
    @skip_on_not_implemented_error
    def test_does_not_crash(
        self: Self,
        populated_store: Store[Delete],
        populated_store_key: str,
    ) -> None:
        populated_store.delete_if_exists(key=populated_store_key)

    @skip_on_not_implemented_error
    def test_does_not_raise_when_attempting_to_delete_non_existent_key(
        self: Self,
        store: Store[Delete],
    ) -> None:
        store.delete_if_exists(key=str(uuid4()))
