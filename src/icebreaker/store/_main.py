from __future__ import annotations

from io import BytesIO
from typing import Self

from icebreaker.store_backends.protocol import Append as Append
from icebreaker.store_backends.protocol import Data as Data
from icebreaker.store_backends.protocol import Delete as Delete
from icebreaker.store_backends.protocol import Path as Path
from icebreaker.store_backends.protocol import PathDoesNotExist as PathDoesNotExist
from icebreaker.store_backends.protocol import PathExists as PathExists
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

    def append(self: Store[Append], path: Path, data: Data) -> None:
        """
        Append data to the existing data at the given path.
        If the path does not exist, the data will be written at the given path.

        Raises:
            StoreBackendDoesNotExist
            PathDoesNotExist
            ConnectionTimeout
            PermissionError
        """
        if not hasattr(self._store_backend, "append"):
            raise NotImplementedError("The store backend does not support append.")
        self._store_backend.append(path=path, data=data)

    def copy(
        from_store: Store[Read],
        to_store: Store[Write],
        from_path: Path,
        to_path: Path,
    ) -> None:
        """
        Copy data between stores.

        Raises:
            StoreBackendDoesNotExist
            PathDoesNotExist
            ConnectionTimeout
            PermissionError
        """
        with from_store.read(path=from_path) as data:
            to_store.write(path=to_path, data=data)

    def delete(
        self: Store[Delete],
        path: Path,
    ) -> None:
        """
        Delete the data at the given path.

        Raises:
            StoreBackendDoesNotExist
            PathDoesNotExist
            ConnectionTimeout
            PermissionError
        """
        if not hasattr(self._store_backend, "delete"):
            raise NotImplementedError("The store backend does not support delete.")
        self._store_backend.delete(path=path)

    def delete_if_exists(
        self: Store[Delete],
        path: Path,
    ) -> None:
        """
        Identical to `delete`, but does not raise an error if the path does not exist.

        Raises:
            StoreBackendDoesNotExist
            ConnectionTimeout
            PermissionError
        """
        try:
            self.delete(path=path)
        except PathDoesNotExist:
            pass

    def read(self: Store[Read], path: Path) -> Data:
        """
        Read data from the store at the given path.

        Raises:
            StoreBackendDoesNotExist
            PathDoesNotExist
            ConnectionTimeout
            ReadTimeout
            PermissionError
        """
        if not hasattr(self._store_backend, "read"):
            raise NotImplementedError("The store backend does not support read.")
        return self._store_backend.read(path=path)

    def read_string(
        self: Store[Read],
        path: Path,
        encoding: str = "utf-8",
    ) -> str:
        """
        Read a string from the store at the given path.

        Raises:
            StoreBackendDoesNotExist
            PathDoesNotExist
            ConnectionTimeout
            ReadTimeout
            PermissionError
        """
        with self.read(path=path) as data:
            return data.read().decode(encoding)

    def write(self: Store[Write], path: Path, data: Data) -> None:
        """
        Write data to the store at the given path.
        If the path already exists, the existing data will be overwritten.

        Raises:
            StoreBackendDoesNotExist
            ConnectionTimeout
            Timeout
            StoreBackendOutOfSpace
            PermissionError
        """
        if not hasattr(self._store_backend, "write"):
            raise NotImplementedError("The store backend does not support write.")
        self._store_backend.write(path=path, data=data)

    def write_if_not_exists(self: Store[WriteIfNotExists], path: Path, data: Data) -> None:
        """
        Atomically write data to the store at the given path if the path does not already exist.

        Raises:
            StoreBackendDoesNotExist
            ConnectionTimeout
            Timeout
            StoreBackendOutOfSpace
            PermissionError
            PathExists
        """
        if not hasattr(self._store_backend, "write_if_not_exists"):
            raise NotImplementedError("The store backend does not support write_if_not_exists.")
        self._store_backend.write_if_not_exists(path=path, data=data)

    def write_string(
        self: Store[Write],
        path: Path,
        data: str,
        encoding: str = "utf-8",
    ) -> None:
        """
        Write a string to the store backend at the given path.
        If the path already exists, the existing data will be overwritten.

        Raises:
            StoreBackendDoesNotExist
            ConnectionTimeout
            Timeout
            StoreBackendOutOfSpace
            PermissionError
        """
        self.write(path=path, data=BytesIO(data.encode(encoding)))
