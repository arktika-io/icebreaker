from typing import Generic
from typing import Self

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


class Store[T]:
    _store_backend: T

    def __init__(
        self: Self,
        store_backend: T,
    ) -> None:
        self._store_backend = store_backend

    @property
    def supports_read(self: Self) -> bool:
        return hasattr(self._store_backend, "read")

    @property
    def supports_write(self: Self) -> bool:
        return hasattr(self._store_backend, "write")

    async def read(self: Self, key: Key) -> Data:
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
        return await self._store_backend.read(key=key)

    async def write(self: Self, key: Key, data: Data) -> None:
        """
        Write data to the store backend at the given key.
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
        await self._store_backend.write(key=key, data=data)
