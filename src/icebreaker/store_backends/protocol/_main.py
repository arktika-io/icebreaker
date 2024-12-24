from pathlib import PurePosixPath
from typing import BinaryIO
from typing import Protocol
from typing import Self
from typing import TypeAlias
from typing import runtime_checkable

Data: TypeAlias = BinaryIO
Path = PurePosixPath


class StoreBackendDoesNotExist(Exception): ...


class PathDoesNotExist(Exception): ...


class PathExists(Exception): ...


class Timeout(Exception): ...


class ConnectionTimeout(Exception): ...


class ReadTimeout(Exception): ...


class StoreBackendOutOfSpace(Exception): ...


PermissionError = PermissionError


@runtime_checkable
class Append(Protocol):
    def append(self: Self, path: Path, data: Data) -> None:
        """
        Append data to the existing data at the given path.
        If the path does not exist, the data will be written at the given path.

        Raises:
            StoreBackendDoesNotExist
            PathDoesNotExist
            ConnectionTimeout
            PermissionError
        """


@runtime_checkable
class Delete(Protocol):
    def delete(self: Self, path: Path) -> None:
        """
        Delete the data at the given path.

        Raises:
            StoreBackendDoesNotExist
            PathDoesNotExist
            ConnectionTimeout
            PermissionError
        """


@runtime_checkable
class Read(Protocol):
    def read(self: Self, path: Path) -> Data:
        """
        Read data from the store at the given path.

        Raises:
            StoreBackendDoesNotExist
            PathDoesNotExist
            ConnectionTimeout
            PermissionError
        """


@runtime_checkable
class Write(Protocol):
    def write(self: Self, path: Path, data: Data) -> None:
        """
        Write data to the store at the given path.

        Raises:
            StoreBackendDoesNotExist
            ConnectionTimeout
            PermissionError
        """


@runtime_checkable
class WriteIfNotExists(Protocol):
    def write_if_not_exists(self: Self, path: Path, data: Data) -> None:
        """
        Write data to the store at the given path if the path does not already exist.

        Raises:
            StoreBackendDoesNotExist
            PathExists
            ConnectionTimeout
            PermissionError
        """


StoreBackend: TypeAlias = Append | Delete | Read | Write | WriteIfNotExists
