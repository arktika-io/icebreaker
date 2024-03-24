import shutil
import subprocess
from typing import Final


class TestCodeFormatting:
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

    def test_code_is_formatted(self) -> None:
        ruff_is_installed: bool = bool(shutil.which("ruff"))
        assert ruff_is_installed, """This test requires ruff (docs.astral.sh/ruff) to be installed.
Please install testing dependencies using "pip install arktika-icebreaker[testing]"."""

        args: list[str] = ["ruff", "check", "."]
        for config in self.RUFF_CONFIG:
            args.extend(["--config", config])

        code_is_formatted: bool = subprocess.run(args).returncode == 0
        assert code_is_formatted, """ruff has found code that hasn't been correctly formatted. 
To see which files are not formatted, check the test output in stdout/stderr.
To automatically apply available fixes, run "icebreaker fmt"."""
