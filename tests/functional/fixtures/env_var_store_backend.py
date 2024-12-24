from uuid import uuid4

import pytest

from icebreaker.store_backends.env_var import EnvVarStoreBackend
from icebreaker.store_backends.protocol import Path


@pytest.fixture(scope="function")
def env_var_store_backend() -> EnvVarStoreBackend:
    return EnvVarStoreBackend(var=Path(str(uuid4())))
