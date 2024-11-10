import pytest
from uuid import uuid4

from icebreaker.store_backends.env_var import EnvVarStoreBackend


@pytest.fixture(scope="function")
def env_var_store_backend() -> EnvVarStoreBackend:
    return EnvVarStoreBackend(var=str(uuid4()))
