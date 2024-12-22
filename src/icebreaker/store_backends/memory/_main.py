from io import BytesIO
from threading import RLock
from typing import Self
from typing import TypeAlias

from icebreaker.store_backends.protocol import Data
from icebreaker.store_backends.protocol import Key
from icebreaker.store_backends.protocol import KeyDoesNotExist
from icebreaker.store_backends.protocol import KeyExists
from icebreaker.store_backends.protocol import StoreBackendOutOfSpace

DataStore: TypeAlias = dict[Key, bytes]


class MemoryStoreBackend:
    _data_store: DataStore
    _lock: RLock

    def __init__(
        self: Self,
        data_store: DataStore | None = None,
        lock: "RLock | None" = None,
    ) -> None:
        self._data_store = data_store or dict()
        self._lock = lock or RLock()

    def delete(self: Self, key: Key) -> None:
        with self._lock:
            try:
                del self._data_store[key]
            except KeyError:
                raise KeyDoesNotExist(key)

    def read(self: Self, key: Key) -> Data:
        with self._lock:
            try:
                return BytesIO(self._data_store[key])
            except KeyError:
                raise KeyDoesNotExist(key)

    def write(self: Self, key: Key, data: Data) -> None:
        with self._lock:
            try:
                self._data_store[key] = data.read()
            except MemoryError:
                raise StoreBackendOutOfSpace()

    def write_if_not_exists(self: Self, key: Key, data: Data) -> None:
        with self._lock:
            if key in self._data_store:
                raise KeyExists(key)
            try:
                self._data_store[key] = data.read()
            except MemoryError:
                raise StoreBackendOutOfSpace()
