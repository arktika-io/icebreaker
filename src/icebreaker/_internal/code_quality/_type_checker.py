from typing import Self
from typing import TypeAlias
from pathlib import Path

Success: TypeAlias = bool
Report: TypeAlias = str
CheckReport: TypeAlias = tuple[Success, Report]


class TypeChecker:
    dependencies_are_installed: bool

    def check(
        self: Self,
        target: Path,
    ) -> CheckReport: ...
