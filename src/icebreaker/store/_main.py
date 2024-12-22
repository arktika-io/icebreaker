from __future__ import annotations

from typing import Self
from io import BytesIO

from icebreaker.store_backends.protocol import Key as Key
from icebreaker.store_backends.protocol import Data as Data
from icebreaker.store_backends.protocol import StoreBackendDoesNotExist as StoreBackendDoesNotExist
from icebreaker.store_backends.protocol import InvalidKey as InvalidKey
from icebreaker.store_backends.protocol import KeyDoesNotExist as KeyDoesNotExist
from icebreaker.store_backends.protocol import KeyExists as KeyExists
from icebreaker.store_backends.protocol import Timeout as Timeout
from icebreaker.store_backends.protocol import StoreBackendOutOfSpace as StoreBackendOutOfSpace
from icebreaker.store_backends.protocol import PermissionError as PermissionError
from icebreaker.store_backends.protocol import Read as Read
from icebreaker.store_backends.protocol import Write as Write
from icebreaker.store_backends.protocol import Delete as Delete
from icebreaker.store_backends.protocol import StoreBackend as StoreBackend


class Store[StoreBackend]:
    _store_backend: StoreBackend

    def __init__(self: Self, store_backend: StoreBackend) -> None:
        self._store_backend = store_backend

    @property
    def supports_read(self: Self) -> bool:
        return hasattr(self._store_backend, "read")

    @property
    def supports_write(self: Self) -> bool:
        return hasattr(self._store_backend, "write")

    @property
    def supports_delete(self: Self) -> bool:
        return hasattr(self._store_backend, "delete")

    def read(self: Store[Read], key: Key) -> Data:
        """
        Read data from the store at the given key.

        Raises:
            StoreBackendDoesNotExist
            InvalidKey
            KeyDoesNotExist
            ConnectionTimeout
            ReadTimeout
            PermissionError
        """
        if not self.supports_read:
            raise NotImplementedError()
        return self._store_backend.read(key=key)

    def read_string(
        self: Store[Read],
        key: Key,
        encoding: str = "utf-8",
    ) -> str:
        """
        Read a string from the store at the given key.

        Raises:
            StoreBackendDoesNotExist
            InvalidKey
            KeyDoesNotExist
            ConnectionTimeout
            ReadTimeout
            PermissionError
        """
        with self.read(key=key) as data:
            return data.read().decode(encoding)

    def write(self: Store[Write], key: Key, data: Data) -> None:
        """
        Write data to the store at the given key.
        If the key already exists, the existing data will be overwritten.

        Raises:
            StoreBackendDoesNotExist
            InvalidKey
            ConnectionTimeout
            Timeout
            StoreBackendOutOfSpace
            PermissionError
        """
        if not self.supports_write:
            raise NotImplementedError()
        self._store_backend.write(key=key, data=data)

    def write_string(
        self: Store[Write],
        key: Key,
        data: str,
        encoding: str = "utf-8",
    ) -> None:
        """
        Write a string to the store backend at the given key.
        If the key already exists, the existing data will be overwritten.

        Raises:
            StoreBackendDoesNotExist
            InvalidKey
            ConnectionTimeout
            Timeout
            StoreBackendOutOfSpace
            PermissionError
        """
        self.write(key=key, data=BytesIO(data.encode(encoding)))

    def delete(
        self: Store[Delete],
        key: Key,
    ) -> None:
        """
        Delete the data at the given key.

        Raises:
            StoreBackendDoesNotExist
            InvalidKey
            KeyDoesNotExist
            ConnectionTimeout
            PermissionError
        """
        self._store_backend.delete(key=key)
