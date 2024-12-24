from io import BytesIO
from typing import Self
from uuid import uuid4

from icebreaker.store import Append
from icebreaker.store import Path
from icebreaker.store import Read
from icebreaker.store import Store
from tests.functional.decorators import skip_on_not_implemented_error


class ReadAppend(Read, Append): ...


class TestAppend:
    @skip_on_not_implemented_error
    def test_does_not_crash(self: Self, store: Store[Append]) -> None:
        store.append(path=Path(str(uuid4())), data=BytesIO(b"data"))

    @skip_on_not_implemented_error
    def test_appends_data_to_existing_path(self: Self, store: Store[ReadAppend]) -> None:
        path = Path(str(uuid4()))
        store.append(path=path, data=BytesIO(b"data"))
        store.append(path=path, data=BytesIO(b"data"))
        assert store.read(path=path).read() == b"datadata"

    @skip_on_not_implemented_error
    def test_appends_empty_data_to_existing_path_if_path_exists_and_data_is_empty(
        self: Self,
        store: Store[ReadAppend],
    ) -> None:
        path = Path(str(uuid4()))
        store.append(path=path, data=BytesIO(b"data"))
        store.append(path=path, data=BytesIO(b""))
        assert store.read(path=path).read() == b"data"

    @skip_on_not_implemented_error
    def test_writes_empty_data_to_new_path_if_path_does_not_exist_and_data_is_empty(
        self: Self,
        store: Store[ReadAppend],
    ) -> None:
        path = Path(str(uuid4()))
        store.append(path=path, data=BytesIO(b""))
        assert store.read(path=path).read() == b""
