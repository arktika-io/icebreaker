from pathlib import Path
from typing import Self

from icebreaker._cli.interfaces import ExitCode
from icebreaker._cli.interfaces import Printer
from icebreaker._internal.code_quality import Formatter
from icebreaker._internal.code_quality import CheckReport
from icebreaker._internal.code_quality import FormatReport
from icebreaker._internal.code_quality import Success
from icebreaker._internal.code_quality import Report


class Fmt:
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
        check: bool,
    ) -> ExitCode:
        if not self.formatter.dependencies_are_installed:
            self.error_printer(
                "CLI dependencies are not installed. ",
                'Please run "pip install arktika-icebreaker[cli]" to unlock this functionality.\n',
            )
            return ExitCode(1)

        if check:
            check_report: CheckReport = self.formatter.check(target=target)
            success: Success = check_report[0]
            report: Report = check_report[1]
        else:
            format_report: FormatReport = self.formatter.format(target=target)
            success: Success = format_report[0]
            report: Report = format_report[1]

        if not success:
            self.error_printer(report)
            return ExitCode(1)

        self.printer(report)
        return ExitCode(0)
