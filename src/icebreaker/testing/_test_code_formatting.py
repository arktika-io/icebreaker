from pathlib import Path
from typing import Self

from icebreaker._internal.formatting import Formatter
from icebreaker._internal.formatting import RuffFormatter


class TestCodeFormatting:
    formatter: Formatter = RuffFormatter()

    def test_code_is_formatted(self: Self) -> None:
        assert self.formatter.dependencies_are_installed, """Missing testing dependencies.
Please install testing dependencies using "pip install arktika-icebreaker[testing]"."""

        code_is_formatted, report = self.formatter.check(target=Path.cwd())
        assert code_is_formatted, f"""Formatting issues detected. 

{report}

To automatically apply available fixes, run "icebreaker fmt".
"""
