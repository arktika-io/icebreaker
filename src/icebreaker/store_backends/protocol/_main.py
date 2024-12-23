from typing import BinaryIO
from typing import Protocol
from typing import Self
from typing import TypeAlias
from typing import runtime_checkable

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


@runtime_checkable
class Append(Protocol):
    def append(self: Self, key: Key, data: Data) -> None:
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


@runtime_checkable
class Delete(Protocol):
    def delete(self: Self, key: Key) -> None:
        """
        Delete the data at the given key.

        Raises:
            StoreBackendDoesNotExist
            InvalidKey
            KeyDoesNotExist
            ConnectionTimeout
            PermissionError
        """


@runtime_checkable
class Read(Protocol):
    def read(self: Self, key: Key) -> Data:
        """
        Read data from the store at the given key.

        Raises:
            StoreBackendDoesNotExist
            InvalidKey
            KeyDoesNotExist
            ConnectionTimeout
            PermissionError
        """


@runtime_checkable
class Write(Protocol):
    def write(self: Self, key: Key, data: Data) -> None:
        """
        Write data to the store at the given key.

        Raises:
            StoreBackendDoesNotExist
            InvalidKey
            ConnectionTimeout
            PermissionError
        """


@runtime_checkable
class WriteIfNotExists(Protocol):
    def write_if_not_exists(self: Self, key: Key, data: Data) -> None:
        """
        Write data to the store at the given key if the key does not already exist.

        Raises:
            StoreBackendDoesNotExist
            InvalidKey
            KeyExists
            ConnectionTimeout
            PermissionError
        """


StoreBackend: TypeAlias = Append | Delete | Read | Write | WriteIfNotExists
