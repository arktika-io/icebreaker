from pathlib import Path
import shutil
import subprocess
from typing import Final
from typing import Self

from icebreaker._internal.typing._type_checker import CheckReport


class MypyTypeChecker:
    MYPY_CONFIG: Final[list[str]] = [
        "--strict",
        "--warn-unreachable",
        "--extra-checks",
    ]

    def __init__(
        self: Self,
        mypy_binary_name: str = "mypy",
    ) -> None:
        self.mypy_binary_name = mypy_binary_name

    @property
    def dependencies_are_installed(self: Self) -> bool:
        return bool(shutil.which(self.mypy_binary_name))

    def _error_if_dependencies_are_not_installed(self: Self) -> None:
        if not self.dependencies_are_installed:
            raise FileNotFoundError(f'"{self.mypy_binary_name}" not found.')

    def check(
        self: Self,
        target: Path,
    ) -> CheckReport:
        self._error_if_dependencies_are_not_installed()

        args: list[str] = [self.mypy_binary_name, str(target)]
        for config in self.MYPY_CONFIG:
            args.append(config)

        result = subprocess.run(args, check=False, capture_output=True)
        report = "\n".join([result.stdout.decode("utf-8"), result.stderr.decode("utf-8")])
        if result.returncode == 0:
            return True, report
        return False, report
