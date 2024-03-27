from pathlib import Path
from typing import Self

from icebreaker._cli.interfaces import ExitCode
from icebreaker._cli.interfaces import Printer
from icebreaker._internal.formatting import Formatter


class FmtCheck:
    printer: Printer
    error_printer: Printer
    formatter: Formatter

    def __init__(
        self: Self,
        printer: Printer,
        error_printer: Printer,
        formatter: Formatter,
    ) -> None:
        self.printer = printer
        self.error_printer = error_printer
        self.formatter = formatter

    def __call__(
        self: Self,
        target: Path,
    ) -> ExitCode:
        if not self.formatter.dependencies_are_installed:
            self.error_printer(
                "CLI dependencies are not installed. ",
                'Please run "pip install arktika-icebreaker[cli]" to unlock this functionality.\n',
            )
            return ExitCode(1)

        success, report = self.formatter.check(target=target)

        if not success:
            self.error_printer(report)
            return ExitCode(1)

        self.printer(report)
        return ExitCode(0)
