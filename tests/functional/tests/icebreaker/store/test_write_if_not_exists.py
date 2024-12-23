from io import BytesIO
from typing import Self
from uuid import uuid4

import pytest

from icebreaker.store import KeyExists
from icebreaker.store import Store
from icebreaker.store import WriteIfNotExists
from tests.functional.decorators import skip_on_not_implemented_error


class TestWriteIfNotExists:
    @skip_on_not_implemented_error
    @pytest.mark.parametrize(
        "data",
        [
            b"",
            b"test_data",
        ],
    )
    def test_does_not_crash(
        self: Self,
        store: Store[WriteIfNotExists],
        data: bytes,
    ) -> None:
        store.write_if_not_exists(key=str(uuid4()), data=BytesIO(data))

    @skip_on_not_implemented_error
    def test_raises_key_exists_when_key_exists(
        self: Self,
        populated_store: Store[WriteIfNotExists],
        populated_store_key: str,
    ) -> None:
        with pytest.raises(KeyExists):
            populated_store.write_if_not_exists(key=populated_store_key, data=BytesIO(b""))
