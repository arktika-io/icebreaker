from base64 import b64decode
from base64 import b64encode
from collections.abc import MutableMapping
import gzip
from io import BytesIO
from json import JSONDecoder
from json import JSONEncoder
import os
from threading import RLock
from typing import ClassVar
from typing import Self

from icebreaker.store_backends.env_vars import EnvVarsStoreBackend
from icebreaker.store_backends.protocol import Data
from icebreaker.store_backends.protocol import Key
from icebreaker.store_backends.protocol import KeyDoesNotExist
from icebreaker.store_backends.protocol import KeyExists

_DEFAULT_JSON_ENCODER: JSONEncoder = JSONEncoder()
_DEFAULT_JSON_DECODER: JSONDecoder = JSONDecoder()


class EnvVarStoreBackend:
    """
    Stores data in a single environment variable as a compressed JSON map.
    """

    _encoding: ClassVar[str] = "utf-8"

    _var: str
    _store_backend: EnvVarsStoreBackend
    _json_encoder: JSONEncoder
    _json_decoder: JSONDecoder
    _lock: RLock

    def __init__(
        self: Self,
        var: str,
        env_vars: MutableMapping[str, str] | None = None,
        json_encoder: JSONEncoder = _DEFAULT_JSON_ENCODER,
        json_decoder: JSONDecoder = _DEFAULT_JSON_DECODER,
        lock: "RLock | None" = None,
    ) -> None:
        self._var = var
        self._store_backend = EnvVarsStoreBackend(env_vars=env_vars or os.environ)
        self._json_encoder = json_encoder
        self._json_decoder = json_decoder
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
            all_data = self._load_store()
            try:
                del all_data[key]
                self._save_store(all_data)
            except KeyError:
                raise KeyDoesNotExist(key)

    def read(self: Self, key: Key) -> Data:
        with self._lock:
            all_data = self._load_store()
            try:
                encoded_value = all_data[key]
                return self._decode(encoded_value)
            except KeyError:
                raise KeyDoesNotExist(key)

    def write(self: Self, key: Key, data: Data) -> None:
        with self._lock:
            all_data = self._load_store()
            all_data[key] = self._encode(data)
            self._save_store(all_data)

    def write_if_not_exists(self: Self, key: Key, data: Data) -> None:
        with self._lock:
            if key in self._load_store():
                raise KeyExists(key)
            self.write(key, data)

    def _load_store(self: Self) -> dict[Key, str]:
        try:
            with self._store_backend.read(key=self._var) as data:
                all_data: dict[Key, str] = self._json_decoder.decode(data.read().decode(self._encoding))
                return all_data
        except KeyDoesNotExist:
            return {}

    def _save_store(self: Self, all_data: dict[Key, str]) -> None:
        encoded_data = self._json_encoder.encode(all_data)
        self._store_backend.write(key=self._var, data=BytesIO(encoded_data.encode(self._encoding)))

    def _encode(self: Self, data: Data) -> str:
        return b64encode(gzip.compress(data.read())).decode(self._encoding)

    def _decode(self: Self, data: str) -> BytesIO:
        return BytesIO(gzip.decompress(b64decode(data.encode(self._encoding))))
