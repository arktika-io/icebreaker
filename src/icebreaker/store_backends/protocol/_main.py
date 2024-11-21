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
    async def read(self: Self, key: Key) -> Data: ...


class Write(Protocol):
    async def write(self: Self, key: Key, data: Data) -> None: ...


class Delete(Protocol):
    async def delete(self: Self, key: Key) -> None: ...


StoreBackend: TypeAlias = Read | Write | Delete
