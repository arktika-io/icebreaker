from pathlib import Path
import shutil
import subprocess
from typing import Final
from typing import Self

from icebreaker._internal.formatting._formatter import CheckReport
from icebreaker._internal.formatting._formatter import FormatReport


class RuffFormatter:
    RUFF_CONFIG: Final[list[str]] = [
        "extend-include=['.venv']",
        "indent-width=4",
        "line-length=120",
        "respect-gitignore=true",
        "format.docstring-code-format=true",
        "format.indent-style='space'",
        "lint.isort.force-single-line=true",
        "lint.isort.force-sort-within-sections=true",
    ]

    def __init__(
        self: Self,
        ruff_binary_name: str = "ruff",
    ) -> None:
        self.ruff_binary_name = ruff_binary_name

    @property
    def dependencies_are_installed(self: Self) -> bool:
        return bool(shutil.which(self.ruff_binary_name))

    def _error_if_dependencies_are_not_installed(self: Self) -> None:
        if not self.dependencies_are_installed:
            raise FileNotFoundError(f'"{self.ruff_binary_name}" not found.')

    def format(
        self: Self,
        target: Path,
    ) -> FormatReport:
        self._error_if_dependencies_are_not_installed()

        args: list[str] = [self.ruff_binary_name, "format", str(target)]
        for config in self.RUFF_CONFIG:
            args.extend(["--config", config])

        result = subprocess.run(args, check=False, capture_output=True)
        report = "\n".join([result.stdout.decode("utf-8"), result.stderr.decode("utf-8")])
        if result.returncode == 0:
            return True, report
        return False, report

    def check(
        self: Self,
        target: Path,
    ) -> CheckReport:
        self._error_if_dependencies_are_not_installed()

        args: list[str] = [self.ruff_binary_name, "check", str(target)]
        for config in self.RUFF_CONFIG:
            args.extend(["--config", config])

        result = subprocess.run(args, check=False, capture_output=True)
        report = "\n".join([result.stdout.decode("utf-8"), result.stderr.decode("utf-8")])
        if result.returncode == 0:
            return True, report
        return False, report
