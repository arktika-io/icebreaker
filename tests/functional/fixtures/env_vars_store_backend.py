import pytest

from icebreaker.store_backends.env_vars import EnvVarsStoreBackend


@pytest.fixture(scope="function")
def env_vars_store_backend() -> EnvVarsStoreBackend:
    return EnvVarsStoreBackend()
