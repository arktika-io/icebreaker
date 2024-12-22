from icebreaker.store import Store
from icebreaker.store import Write
from uuid import uuid4
from io import BytesIO
import pytest
from typing import Self


class TestWrite:
    @pytest.mark.parametrize(
        "data",
        [
            b"",
            b"test_data",
        ],
    )
    def test_does_not_crash(
        self: Self,
        store: Store[Write],
        data: bytes,
    ) -> None:
        if not store.supports_write:
            pytest.skip("write not implemented")
        store.write(key=str(uuid4()), data=BytesIO(data))
