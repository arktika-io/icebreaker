from io import BytesIO
from threading import RLock
from typing import Self
from typing import TypeAlias

from icebreaker.store_backends.protocol import Data
from icebreaker.store_backends.protocol import Path
from icebreaker.store_backends.protocol import PathDoesNotExist
from icebreaker.store_backends.protocol import PathExists
from icebreaker.store_backends.protocol import StoreBackendOutOfSpace

DataStore: TypeAlias = dict[Path, bytes]


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

    def append(self: Self, path: Path, data: Data) -> None:
        with self._lock:
            try:
                existing_data = self.read(path=path)
            except PathDoesNotExist:
                existing_data = BytesIO(b"")
            new_data = BytesIO(existing_data.read() + data.read())
            self.write(path=path, data=new_data)

    def delete(self: Self, path: Path) -> None:
        with self._lock:
            try:
                del self._data_store[path]
            except KeyError:
                raise PathDoesNotExist()

    def read(self: Self, path: Path) -> Data:
        with self._lock:
            try:
                return BytesIO(self._data_store[path])
            except KeyError:
                raise PathDoesNotExist()

    def write(self: Self, path: Path, data: Data) -> None:
        with self._lock:
            try:
                self._data_store[path] = data.read()
            except MemoryError:
                raise StoreBackendOutOfSpace()

    def write_if_not_exists(self: Self, path: Path, data: Data) -> None:
        with self._lock:
            if path in self._data_store:
                raise PathExists(path)
            try:
                self._data_store[path] = data.read()
            except MemoryError:
                raise StoreBackendOutOfSpace()
