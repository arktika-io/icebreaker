from pathlib import Path
import shutil
import subprocess
from typing import Self

from icebreaker._cli.interfaces import Printer


class Fmt:
    printer: Printer
    error_printer: Printer

    def __init__(
        self: Self,
        printer: Printer,
        error_printer: Printer,
    ) -> None:
        self.printer = printer
        self.error_printer = error_printer

    def __call__(
        self: Self,
        target: Path,
        check: bool,
    ) -> None:
        dependencies_installed: bool = all([shutil.which("ruff")])
        if not dependencies_installed:
            self.error_printer(
                "CLI dependencies are not installed. ",
                'Please run "pip install icebreaker[cli]" to unlock this functionality.\n',
            )
            raise RuntimeError()

        if check:
            return self._check(target=target)
        else:
            return self._run(target=target)

    def _check(self: Self, target: Path) -> None:
        subprocess.run(
            ["ruff", "check", str(target)],
            check=True,
        )

    def _run(self: Self, target: Path) -> None:
        subprocess.run(
            ["ruff", "format", str(target)],
            check=True,
        )
