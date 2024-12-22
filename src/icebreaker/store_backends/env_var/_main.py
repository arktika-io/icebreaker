from typing import Self
from io import BytesIO
from collections.abc import MutableMapping
import json
from base64 import b64encode
from base64 import b64decode
import gzip

from icebreaker.store_backends.protocol import KeyDoesNotExist
from icebreaker.store_backends.protocol import Key
from icebreaker.store_backends.protocol import Data
from icebreaker.store_backends.env_vars import EnvVarsStoreBackend


class EnvVarStoreBackend:
    _var: str
    _store_backend: EnvVarsStoreBackend
    _encoding: str = "utf-8"

    def __init__(
        self: Self,
        var: str,
        env_vars: MutableMapping[str, str] | None = None,
    ) -> None:
        self._var = var
        self._store_backend = EnvVarsStoreBackend(env_vars=env_vars)

    def read(self: Self, key: Key) -> Data:
        try:
            data = self._store_backend.read(key=self._var)
            loaded_data = json.loads(data.read().decode("utf-8"))
            return self._decode(data=loaded_data[key])
        except KeyError:
            raise KeyDoesNotExist(key)

    def write(self: Self, key: Key, data: Data) -> None:
        try:
            old_data_file_obj = self._store_backend.read(key=self._var)
            old_data = old_data_file_obj.read()
            old_data_decoded = json.loads(old_data.decode("utf-8"))
        except KeyDoesNotExist:
            old_data_decoded = {}

        old_data_decoded[key] = self._encode(data=data)
        old_data_encoded = json.dumps(old_data_decoded).encode("utf-8")
        self._store_backend.write(key=self._var, data=BytesIO(old_data_encoded))

    def delete(self: Self, key: Key) -> None:
        try:
            old_data_file_obj = self._store_backend.read(key=self._var)
            old_data = old_data_file_obj.read()
            old_data_decoded = json.loads(old_data.decode("utf-8"))
            del old_data_decoded[key]
            old_data_encoded = json.dumps(old_data_decoded).encode("utf-8")
            self._store_backend.write(key=self._var, data=BytesIO(old_data_encoded))
        except KeyError:
            raise KeyDoesNotExist(key)

    def _encode(self: Self, data: Data) -> str:
        return b64encode(gzip.compress(data.read())).decode(self._encoding)

    def _decode(self: Self, data: str) -> BytesIO:
        return BytesIO(gzip.decompress(b64decode(data.encode(self._encoding))))
