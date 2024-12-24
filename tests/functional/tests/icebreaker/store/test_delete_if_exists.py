from typing import Self
from uuid import uuid4

from icebreaker.store import Delete
from icebreaker.store import Path
from icebreaker.store import Store
from tests.functional.decorators import skip_on_not_implemented_error


class TestDeleteIfExists:
    @skip_on_not_implemented_error
    def test_does_not_crash(
        self: Self,
        populated_store: Store[Delete],
        populated_store_path: Path,
    ) -> None:
        populated_store.delete_if_exists(path=populated_store_path)

    @skip_on_not_implemented_error
    def test_does_not_raise_when_attempting_to_delete_non_existent_path(
        self: Self,
        store: Store[Delete],
    ) -> None:
        store.delete_if_exists(path=Path(str(uuid4())))
