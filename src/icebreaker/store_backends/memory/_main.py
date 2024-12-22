from typing import Self
from typing import TypeAlias
from io import BytesIO

from icebreaker.store_backends.protocol import KeyDoesNotExist
from icebreaker.store_backends.protocol import Key
from icebreaker.store_backends.protocol import Data
from icebreaker.store_backends.protocol import StoreBackendOutOfSpace

DataStore: TypeAlias = dict[Key, bytes]


class MemoryStoreBackend:
    _data_store: DataStore

    def __init__(
        self: Self,
        data_store: DataStore | None = None,
    ) -> None:
        self._data_store = data_store or dict()

    def read(self: Self, key: Key) -> Data:
        try:
            return BytesIO(self._data_store[key])
        except KeyError:
            raise KeyDoesNotExist(key)

    def write(self: Self, key: Key, data: Data) -> None:
        try:
            self._data_store[key] = data.read()
        except MemoryError:
            raise StoreBackendOutOfSpace()

    def delete(self: Self, key: Key) -> None:
        try:
            del self._data_store[key]
        except KeyError:
            raise KeyDoesNotExist(key)
