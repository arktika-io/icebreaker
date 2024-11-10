from typing import BinaryIO
from typing import Protocol
from typing import Self
from typing import TypeAlias

Key = str
Data: TypeAlias = BinaryIO


class StoreBackendDoesNotExist(Exception): ...


class InvalidKey(Exception): ...


class KeyDoesNotExist(Exception): ...


class KeyExists(Exception): ...


class Timeout(Exception): ...


class ConnectionTimeout(Exception): ...


class ReadTimeout(Exception): ...


class StoreBackendOutOfSpace(Exception): ...


PermissionError = PermissionError


class Read(Protocol):
    async def read(self: Self, key: Key) -> Data:
        """
        Read data from the store backend at the given key.

        Raises:
            StoreBackendDoesNotExist
            InvalidKey
            KeyDoesNotExist
            ConnectionTimeout
            ReadTimeout
            PermissionError
        """


class Write(Protocol):
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
