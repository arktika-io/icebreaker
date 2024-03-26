from typing import Self
from pathlib import Path

from icebreaker._internal.typing import MypyTypeChecker
from icebreaker._internal.typing import TypeChecker


class TestCodeTyping:
    type_checker: TypeChecker = MypyTypeChecker()

    def test_code_is_correctly_typed(self: Self) -> None:
        assert self.type_checker.dependencies_are_installed, """Missing testing dependencies.
Please install testing dependencies using "pip install arktika-icebreaker[testing]"."""

        code_is_correctly_typed, report = self.type_checker.check(target=Path.cwd())
        assert code_is_correctly_typed, f"""Typing issues detected.

{report}"""
