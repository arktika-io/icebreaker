from typing import Self
from uuid import uuid4

import pytest

from icebreaker.store import KeyDoesNotExist
from icebreaker.store import Read
from icebreaker.store import Store
from tests.functional.decorators import skip_on_not_implemented_error


class TestRead:
    @skip_on_not_implemented_error
    def test_does_not_crash(
        self: Self,
        populated_store: Store[Read],
        populated_store_key: str,
    ) -> None:
        populated_store.read(key=populated_store_key)

    @skip_on_not_implemented_error
    def test_does_not_crash_as_a_context_manager(
        self: Self,
        populated_store: Store[Read],
        populated_store_key: str,
    ) -> None:
        with populated_store.read(key=populated_store_key) as data:
            assert data.read()
        assert data.closed

    @skip_on_not_implemented_error
    def test_raises_key_does_not_exist_when_attempting_to_read_non_existent_key(
        self: Self,
        store: Store[Read],
    ) -> None:
        with pytest.raises(KeyDoesNotExist):
            store.read(key=str(uuid4()))
