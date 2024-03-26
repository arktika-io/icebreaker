from typing import Self
from typing import TypeAlias
from typing import Protocol
from pathlib import Path

Success: TypeAlias = bool
Report: TypeAlias = str
CheckReport: TypeAlias = tuple[Success, Report]
FormatReport: TypeAlias = tuple[Success, Report]


class Formatter(Protocol):
    @property
    def dependencies_are_installed(self: Self) -> bool: ...

    def format(
        self: Self,
        target: Path,
    ) -> FormatReport: ...

    def check(
        self: Self,
        target: Path,
    ) -> CheckReport: ...
