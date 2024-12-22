from io import BytesIO
from typing import Self
from uuid import uuid4

import pytest

from icebreaker.store import Store
from icebreaker.store import Write


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
        store_implementing_write: Store[Write],
        data: bytes,
    ) -> None:
        store_implementing_write.write(key=str(uuid4()), data=BytesIO(data))
