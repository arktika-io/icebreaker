from io import BytesIO
from typing import Self
from uuid import uuid4

import pytest

from icebreaker.store import Path
from icebreaker.store import Store
from icebreaker.store import Write
from tests.functional.decorators import skip_on_not_implemented_error


class TestWrite:
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
        store: Store[Write],
        data: bytes,
    ) -> None:
        store.write(path=Path(str(uuid4())), data=BytesIO(data))
