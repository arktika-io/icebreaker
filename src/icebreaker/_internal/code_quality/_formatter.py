from typing import Self
from typing import TypeAlias
from pathlib import Path

Success: TypeAlias = bool
Report: TypeAlias = str
CheckReport: TypeAlias = tuple[Success, Report]
FormatReport: TypeAlias = tuple[Success, Report]


class Formatter:
    dependencies_are_installed: bool

    def format(
        self: Self,
        target: Path,
    ) -> FormatReport: ...

    def check(
        self: Self,
        target: Path,
    ) -> CheckReport: ...
