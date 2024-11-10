import os
from typing import Self
from io import BytesIO
from collections.abc import MutableMapping
from base64 import b64encode
from base64 import b64decode
import gzip

from icebreaker.store_backends.protocol import KeyDoesNotExist
from icebreaker.store_backends.protocol import Key
from icebreaker.store_backends.protocol import Data


class EnvVarsStoreBackend:
    _env_vars: MutableMapping[str, str]
    _encoding: str = "utf-8"

    def __init__(
        self: Self,
        env_vars: MutableMapping[str, str] | None = None,
    ) -> None:
        self._env_vars = env_vars or os.environ

    async def read(self: Self, key: Key) -> Data:
        try:
            return self._decode(self._env_vars[key])
        except KeyError:
            raise KeyDoesNotExist(key)

    async def write(self: Self, key: Key, data: Data) -> None:
        self._env_vars[key] = self._encode(data)

    def _encode(self: Self, data: Data) -> str:
        return b64encode(gzip.compress(data.read())).decode(self._encoding)

    def _decode(self: Self, data: str) -> BytesIO:
        return BytesIO(gzip.decompress(b64decode(data.encode(self._encoding))))
