from io import BytesIO
from typing import Self
from uuid import uuid4

import pytest

from icebreaker.store import Path
from icebreaker.store import PathExists
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
        store.write_if_not_exists(path=Path(str(uuid4())), data=BytesIO(data))

    @skip_on_not_implemented_error
    def test_raises_path_exists_when_path_exists(
        self: Self,
        populated_store: Store[WriteIfNotExists],
        populated_store_path: Path,
    ) -> None:
        with pytest.raises(PathExists):
            populated_store.write_if_not_exists(path=populated_store_path, data=BytesIO(b""))
