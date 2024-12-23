from __future__ import annotations

from io import BytesIO
from typing import Self

from icebreaker.store_backends.protocol import Append as Append
from icebreaker.store_backends.protocol import Data as Data
from icebreaker.store_backends.protocol import Delete as Delete
from icebreaker.store_backends.protocol import InvalidKey as InvalidKey
from icebreaker.store_backends.protocol import Key as Key
from icebreaker.store_backends.protocol import KeyDoesNotExist as KeyDoesNotExist
from icebreaker.store_backends.protocol import KeyExists as KeyExists
from icebreaker.store_backends.protocol import PermissionError as PermissionError
from icebreaker.store_backends.protocol import Read as Read
from icebreaker.store_backends.protocol import StoreBackend as StoreBackend
from icebreaker.store_backends.protocol import StoreBackendDoesNotExist as StoreBackendDoesNotExist
from icebreaker.store_backends.protocol import StoreBackendOutOfSpace as StoreBackendOutOfSpace
from icebreaker.store_backends.protocol import Timeout as Timeout
from icebreaker.store_backends.protocol import Write as Write
from icebreaker.store_backends.protocol import WriteIfNotExists as WriteIfNotExists


class Store[StoreBackend]:
    _store_backend: StoreBackend

    def __init__(self: Self, store_backend: StoreBackend) -> None:
        self._store_backend = store_backend

    def append(self: Store[Append], key: Key, data: Data) -> None:
        """
        Append data to the existing data at the given key.
        If the key does not exist, the data will be written at the given key.

        Raises:
            StoreBackendDoesNotExist
            InvalidKey
            KeyDoesNotExist
            ConnectionTimeout
            PermissionError
        """
        if not hasattr(self._store_backend, "append"):
            raise NotImplementedError("The store backend does not support append.")
        self._store_backend.append(key=key, data=data)

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
        if not hasattr(self._store_backend, "delete"):
            raise NotImplementedError("The store backend does not support delete.")
        self._store_backend.delete(key=key)

    def delete_if_exists(
        self: Store[Delete],
        key: Key,
    ) -> None:
        """
        Identical to `delete`, but does not raise an error if the key does not exist.

        Raises:
            StoreBackendDoesNotExist
            InvalidKey
            ConnectionTimeout
            PermissionError
        """
        try:
            self.delete(key=key)
        except KeyDoesNotExist:
            pass

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
        if not hasattr(self._store_backend, "read"):
            raise NotImplementedError("The store backend does not support read.")
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
        if not hasattr(self._store_backend, "write"):
            raise NotImplementedError("The store backend does not support write.")
        self._store_backend.write(key=key, data=data)

    def write_if_not_exists(self: Store[WriteIfNotExists], key: Key, data: Data) -> None:
        """
        Atomically write data to the store at the given key if the key does not already exist.

        Raises:
            StoreBackendDoesNotExist
            InvalidKey
            ConnectionTimeout
            Timeout
            StoreBackendOutOfSpace
            PermissionError
            KeyExists
        """
        if not hasattr(self._store_backend, "write_if_not_exists"):
            raise NotImplementedError("The store backend does not support write_if_not_exists.")
        self._store_backend.write_if_not_exists(key=key, data=data)

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
