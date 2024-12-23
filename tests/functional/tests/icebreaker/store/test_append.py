from io import BytesIO
from typing import Self
from uuid import uuid4

import pytest

from icebreaker.store import Append
from icebreaker.store import KeyDoesNotExist
from icebreaker.store import Store


class TestAppend:
    def test_does_not_crash(self: Self, store_implementing_append: Store[Append]) -> None:
        store_implementing_append.append(key=str(uuid4()), data=BytesIO(b"data"))

    def test_appends_data_to_existing_key(self: Self, store_implementing_append: Store[Append]) -> None:
        key = str(uuid4())
        store_implementing_append.append(key=key, data=BytesIO(b"data"))
        store_implementing_append.append(key=key, data=BytesIO(b"data"))
        assert store_implementing_append.read(key=key).read() == b"datadata"

    def test_appends_empty_data_to_existing_key_if_key_exists_and_data_is_empty(
        self: Self, store_implementing_append: Store[Append]
    ) -> None:
        key = str(uuid4())
        store_implementing_append.append(key=key, data=BytesIO(b"data"))
        store_implementing_append.append(key=key, data=BytesIO(b""))
        assert store_implementing_append.read(key=key).read() == b"data"

    def test_writes_empty_data_to_new_key_if_key_does_not_exist_and_data_is_empty(
        self: Self, store_implementing_append: Store[Append]
    ) -> None:
        key = str(uuid4())
        store_implementing_append.append(key=key, data=BytesIO(b""))
        assert store_implementing_append.read(key=key).read() == b""
