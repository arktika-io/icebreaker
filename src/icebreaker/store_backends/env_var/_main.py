from typing import ClassVar, Self
from io import BytesIO
from collections.abc import MutableMapping
import gzip
import os
from base64 import b64encode, b64decode
from json import JSONEncoder
from json import JSONDecoder
from threading import RLock

from icebreaker.store_backends.protocol import KeyDoesNotExist, Key, Data
from icebreaker.store_backends.env_vars import EnvVarsStoreBackend
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

    def delete(self: Self, key: Key) -> None:
        with self._lock:
            all_data = self._load_store()
            try:
                del all_data[key]
                self._save_store(all_data)
            except KeyError:
                raise KeyDoesNotExist(key)

    def _load_store(self) -> dict:
        try:
            with self._store_backend.read(key=self._var) as data:
                return self._json_decoder.decode(data.read().decode(self._encoding))
        except KeyDoesNotExist:
            return {}

    def _save_store(self, all_data: dict) -> None:
        encoded_data = self._json_encoder.encode(all_data)
        self._store_backend.write(key=self._var, data=BytesIO(encoded_data.encode(self._encoding)))

    def _encode(self, data: Data) -> str:
        return b64encode(gzip.compress(data.read())).decode(self._encoding)

    def _decode(self, data: str) -> BytesIO:
        return BytesIO(gzip.decompress(b64decode(data.encode(self._encoding))))
