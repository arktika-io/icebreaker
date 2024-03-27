from argparse import ArgumentParser
from argparse import Namespace
from collections.abc import Callable
import functools
from pathlib import Path
import traceback
from typing import Any
from typing import Self
from typing import TypeAlias

from icebreaker._cli.commands.fmt import Fmt
from icebreaker._cli.commands.fmt_check import FmtCheck
from icebreaker._cli.commands.version import Version
from icebreaker._cli.interfaces import ExitCode
from icebreaker._cli.interfaces import Printer
from icebreaker._cli.interfaces import Reader
from icebreaker._internal.formatting import Formatter

Command: TypeAlias = str
Subcommand: TypeAlias = str | None
Arguments: TypeAlias = dict[str, Any]
Handler: TypeAlias = Callable[[], ExitCode]


class CLI:
    printer: Printer
    error_printer: Printer
    reader: Reader
    formatter: Formatter

    def __init__(
        self: Self,
        printer: Printer,
        error_printer: Printer,
        reader: Reader,
        formatter: Formatter,
    ) -> None:
        self.printer = printer
        self.error_printer = error_printer
        self.reader = reader
        self.formatter = formatter

    def __call__(self: Self) -> ExitCode:
        command, subcommand, arguments = self._get_called_command_and_arguments()
        handler: Handler | None = self._get_handler(command=command, subcommand=subcommand, arguments=arguments)

        if handler is None:
            self.error_printer(f"Unknown command: {command}\n")
            return ExitCode(1)

        try:
            exit_code = handler()
        except BaseException:
            self.error_printer(traceback.format_exc())
            exit_code = ExitCode(1)

        return exit_code

    def _get_called_command_and_arguments(self: Self) -> tuple[Command, Subcommand, Arguments]:
        root_argument_parser: ArgumentParser = ArgumentParser(
            prog="icebreaker",
            description="Icebreaker CLI.",
            exit_on_error=False,
        )
        root_subparsers: Any = root_argument_parser.add_subparsers(title="Commands", dest="command")

        # Add "fmt" command
        fmt_parser: ArgumentParser = root_subparsers.add_parser(
            name="fmt",
            description="Format the codebase.",
        )
        fmt_parser.add_argument("--target", metavar="TARGET", default=".", type=Path)

        fmt_subparsers: Any = fmt_parser.add_subparsers(title="subcommands", dest="subcommand")

        # Add "fmt check" command
        fmt_check_parser: ArgumentParser = fmt_subparsers.add_parser(
            name="check", description="Check the formatting of the codebase."
        )
        fmt_check_parser.add_argument("--target", metavar="TARGET", default=".", type=Path)

        # Add "version" command
        root_subparsers.add_parser(name="version", description="Show version number and quit.")

        parsed_arguments: Namespace = root_argument_parser.parse_args()
        arguments: Arguments = vars(parsed_arguments)
        command: Command = arguments.pop("command")
        subcommand: Subcommand = arguments.pop("subcommand") if "subcommand" in arguments else None
        return command, subcommand, arguments

    def _get_handler(self: Self, command: Command, subcommand: Subcommand, arguments: Arguments) -> Handler | None:
        handler: Handler | None = None
        if command == "version":
            handler = functools.partial(Version(printer=self.printer).__call__, **arguments)
        elif command == "fmt":
            if subcommand == "check":
                handler = functools.partial(
                    FmtCheck(printer=self.printer, error_printer=self.error_printer, formatter=self.formatter),
                    **arguments,
                )
            else:
                handler = functools.partial(
                    Fmt(printer=self.printer, error_printer=self.error_printer, formatter=self.formatter), **arguments
                )
        return handler
