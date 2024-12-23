from base64 import b64decode
from base64 import b64encode
from collections.abc import MutableMapping
import gzip
from io import BytesIO
import os
from threading import RLock
from typing import ClassVar
from typing import Self

from icebreaker.store_backends.protocol import Data
from icebreaker.store_backends.protocol import Key
from icebreaker.store_backends.protocol import KeyDoesNotExist
from icebreaker.store_backends.protocol import KeyExists


class EnvVarsStoreBackend:
    _encoding: ClassVar[str] = "utf-8"

    _env_vars: MutableMapping[str, str]
    _lock: RLock

    def __init__(
        self: Self,
        env_vars: MutableMapping[str, str] | None = None,
        lock: "RLock | None" = None,
    ) -> None:
        self._env_vars = env_vars or os.environ
        self._lock = lock or RLock()

    def append(self: Self, key: Key, data: Data) -> None:
        with self._lock:
            try:
                existing_data = self.read(key=key)
            except KeyDoesNotExist:
                existing_data = BytesIO(b"")
            new_data = BytesIO(existing_data.read() + data.read())
            self.write(key=key, data=new_data)

    def delete(self: Self, key: Key) -> None:
        with self._lock:
            try:
                del self._env_vars[key]
            except KeyError:
                raise KeyDoesNotExist(key)

    def read(self: Self, key: Key) -> Data:
        with self._lock:
            try:
                return self._decode(self._env_vars[key])
            except KeyError:
                raise KeyDoesNotExist(key)

    def write(self: Self, key: Key, data: Data) -> None:
        with self._lock:
            self._env_vars[key] = self._encode(data)

    def write_if_not_exists(self: Self, key: Key, data: Data) -> None:
        with self._lock:
            if key in self._env_vars:
                raise KeyExists(key)
            self._env_vars[key] = self._encode(data)

    def _encode(self: Self, data: Data) -> str:
        return b64encode(gzip.compress(data.read())).decode(self._encoding)

    def _decode(self: Self, data: str) -> BytesIO:
        return BytesIO(gzip.decompress(b64decode(data.encode(self._encoding))))
