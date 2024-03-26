from typing import Self
from pathlib import Path

from icebreaker._internal.code_quality import RuffFormatter as RuffFormatter
from icebreaker._internal.code_quality import Formatter as Formatter
from icebreaker._internal.code_quality import CheckReport
from icebreaker._internal.code_quality import FormatReport
from icebreaker._internal.code_quality import Success
from icebreaker._internal.code_quality import Report


class TestCodeFormatting:
    formatter: Formatter = RuffFormatter()

    def test_code_is_formatted(self: Self) -> None:
        assert self.formatter.dependencies_are_installed, """Missing testing dependencies.
Please install testing dependencies using "pip install arktika-icebreaker[testing]"."""

        check_report: CheckReport = self.formatter.check(target=Path.cwd())
        code_is_formatted: Success = check_report[0]
        report: Report = check_report[1]
        assert code_is_formatted, f"""Formatting issues found. 

{report}

To automatically apply available fixes, run "icebreaker fmt".
"""
