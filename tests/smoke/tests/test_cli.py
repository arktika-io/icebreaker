import subprocess
from subprocess import CompletedProcess
from typing import Self

from icebreaker import __version__


class TestCLIVersion:
    def test_returns_expected_output(self: Self) -> None:
        output: CompletedProcess[str] = subprocess.run(
            ["icebreaker", "version"],
            check=True,
            text=True,
            capture_output=True,
        )
        assert output.stdout == __version__

    def test_returns_expected_status_code(self: Self) -> None:
        output: CompletedProcess[str] = subprocess.run(
            ["icebreaker", "version"],
            check=False,
            text=True,
            capture_output=True,
        )
        assert output.returncode == 0
