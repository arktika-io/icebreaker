from io import BytesIO
from typing import Self
from uuid import uuid4

import pytest

from icebreaker.store import KeyExists
from icebreaker.store import Store
from icebreaker.store import WriteIfNotExists


class TestWriteIfNotExists:
    @pytest.mark.parametrize(
        "data",
        [
            b"",
            b"test_data",
        ],
    )
    def test_does_not_crash(
        self: Self,
        store_implementing_write_if_not_exists: Store[WriteIfNotExists],
        data: bytes,
    ) -> None:
        store_implementing_write_if_not_exists.write_if_not_exists(key=str(uuid4()), data=BytesIO(data))

    def test_raises_key_exists_when_key_exists(
        self: Self,
        populated_store_implementing_write_if_not_exists: Store[WriteIfNotExists],
        populated_store_key: str,
    ) -> None:
        with pytest.raises(KeyExists):
            populated_store_implementing_write_if_not_exists.write_if_not_exists(
                key=populated_store_key, data=BytesIO(b"")
            )
