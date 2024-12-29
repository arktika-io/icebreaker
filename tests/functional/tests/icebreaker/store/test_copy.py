from typing import Self
from uuid import uuid4

from icebreaker.store import Path
from icebreaker.store import Read
from icebreaker.store import Store
from icebreaker.store import Write
from tests.functional.decorators import skip_on_not_implemented_error


class ReadWrite(Read, Write): ...


class TestCopy:
    @skip_on_not_implemented_error
    def test_does_not_crash_when_copying_to_the_same_path_in_the_same_store(
        self: Self,
        populated_store: Store[ReadWrite],
        populated_store_path: Path,
    ) -> None:
        populated_store.copy(
            to_store=populated_store,
            from_path=populated_store_path,
            to_path=populated_store_path,
        )

    @skip_on_not_implemented_error
    def test_does_not_crash_when_copying_to_a_different_path_in_the_same_store(
        self: Self,
        populated_store: Store[ReadWrite],
        populated_store_path: Path,
    ) -> None:
        populated_store.copy(
            to_store=populated_store,
            from_path=populated_store_path,
            to_path=Path(str(uuid4())),
        )

    @skip_on_not_implemented_error
    def test_does_not_crash_when_copying_to_the_same_path_in_a_different_store(
        self: Self,
        populated_store: Store[Read],
        populated_store_path: Path,
        store: Store[Write],
    ) -> None:
        populated_store.copy(
            to_store=store,
            from_path=populated_store_path,
            to_path=populated_store_path,
        )

    @skip_on_not_implemented_error
    def test_does_not_crash_when_copying_to_a_different_path_in_a_different_store(
        self: Self,
        populated_store: Store[Read],
        populated_store_path: Path,
        store: Store[Write],
    ) -> None:
        populated_store.copy(
            to_store=store,
            from_path=populated_store_path,
            to_path=Path(str(uuid4())),
        )
