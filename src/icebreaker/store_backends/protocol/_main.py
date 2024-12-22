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


class Delete(Protocol):
    def delete(self: Self, key: Key) -> None: ...


class Read(Protocol):
    def read(self: Self, key: Key) -> Data: ...


class Write(Protocol):
    def write(self: Self, key: Key, data: Data) -> None: ...


class WriteIfNotExists(Protocol):
    def write_if_not_exists(self: Self, key: Key, data: Data) -> None: ...


StoreBackend: TypeAlias = Delete | Read | Write | WriteIfNotExists
