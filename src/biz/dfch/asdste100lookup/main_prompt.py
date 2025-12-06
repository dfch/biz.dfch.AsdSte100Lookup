# Copyright (c) 2025 Ronald Rink, http://d-fens.ch
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""MainPrompt class."""

from __future__ import annotations
import argparse
from datetime import datetime
from pathlib import Path
import shlex
import tempfile


from .commands.command_base import CommandBase
from .commands.command_query_type import CommandQueryType
from .commands.empty_command import EmptyCommand
from .commands.exit_command import ExitCommand
from .commands.help_command import HelpCommand
from .commands.rule_command import RuleCommand
from .commands.save_command import SaveCommand
from .commands.unknown_command import UnknownCommand
from .commands.word_category_command import WordCategoryCommand


class MainPrompt:  # pylint: disable=R0903
    """Represents the main prompt processing."""

    _start_of_command: str = "!"
    _category_command_names = ["category", "c"]
    _rule_command_names = ["rule", "r"]
    _save_command_names = ["save", "s"]
    _filter_command_names = ["filter", "f"]

    _parser: argparse.ArgumentParser

    def __init__(self):
        self._parser = self._build_parser()

    class SuppressErrorMessageArgumentParser(argparse.ArgumentParser):
        """Suppress error messages while parsing."""

        def error(self, _: str) -> None:  # type: ignore[override]
            # We raise SystemExit and catch that inside `parse_command()`.
            raise SystemExit

    def _build_parser(self) -> argparse.ArgumentParser:
        """Builds the argument parser for the main prompt."""

        result = MainPrompt.SuppressErrorMessageArgumentParser(
            prog="Main-prompt",
            description="Enter a search term (regular expression) "
            "or press <ENTER> to exit. "
            f"Or start a command with '{self._start_of_command}' "
            "(eg. '! save').",
            add_help=True,
        )

        subparsers_action = result.add_subparsers(
            dest="command", required=True, help="Available commands."
        )
        category_parser = subparsers_action.add_parser(
            self._category_command_names[0],
            aliases=self._category_command_names[1:],
            help="This command shows all words from the specified category.",
        )

        category_parser_args = category_parser.add_mutually_exclusive_group(
            required=True
        )
        category_parser_args.add_argument(
            "-i",
            "--id",
            help="Id (short name) of the word category to query.",
        )

        category_parser_args.add_argument(
            "-n",
            "--name",
            help="Name of the word category to query.",
        )

        rule_parser = subparsers_action.add_parser(
            self._rule_command_names[0],
            aliases=self._rule_command_names[1:],
            help="This command shows the specified rule.",
        )

        rule_parser_args = rule_parser.add_mutually_exclusive_group(
            required=True
        )
        rule_parser_args.add_argument(
            "-i",
            "--id",
            help="Id of the rule to query.",
        )

        rule_parser_args.add_argument(
            "-n",
            "--name",
            help="Name of the rule to query.",
        )

        rule_parser_args.add_argument(
            "-s",
            "--section",
            help="Section of the rule to query.",
        )

        rule_parser_args.add_argument(
            "-c",
            "--category",
            help="Category of the rule to query.",
        )

        rule_parser_args.add_argument(
            "--summary",
            help="Summary of the rule to query.",
        )

        rule_parser.add_argument(
            "-b",
            "--brief",
            action="store_true",
            help="Display only a brief overview of matching rules.",
        )

        save_parser = subparsers_action.add_parser(
            self._save_command_names[0],
            aliases=self._save_command_names[1:],
            help="This command writes the last console output to a file.",
        )

        save_parser_args = save_parser.add_mutually_exclusive_group(
            required=True
        )

        save_parser_args.add_argument(
            "-n",
            "--name",
            help="Give the name of the file.",
        )

        save_parser_args.add_argument(
            "-a",
            "--auto",
            action="store_true",
            help="Automatically select a unique name for the file.",
        )

        group = result.add_mutually_exclusive_group()

        group.add_argument(
            "--exit",
            dest="exit",
            action="store_true",
            help="This command stops the programme.",
        )

        return result

    def parse(self, text: str) -> CommandBase:
        """Parses a line of text into a command."""

        if not isinstance(text, str) or "" == text.strip():
            return EmptyCommand("")

        text = text.strip()

        if text in ["?", "-h", "--help"]:
            return HelpCommand(self._parser.format_help())

        # If the line does not starts with '!', we expect a dictionary lookup.
        if not text.startswith(self._start_of_command):
            return UnknownCommand(text)

        # First, split the input line into args.
        text = text.strip(self._start_of_command)
        try:
            args = shlex.split(text)
        except ValueError:
            return UnknownCommand(text)

        # Second, try to parse it into the defined arguments.
        try:
            ns = self._parser.parse_args(args)
        # Suppress SONAR warning, as we expect this exception from ArgParse, if
        # the user types in something else than a defined command or argument.
        # In that case, we want to parse the contents and display a word from
        # the dicionary. This is intended.
        except SystemExit as ex:  # NOSONAR
            if "0" == str(ex):
                return HelpCommand("")

            return HelpCommand(self._parser.format_help())

        if ns.command is not None:
            if ns.command in self._category_command_names:
                if ns.id is not None:
                    return WordCategoryCommand(CommandQueryType.ID, ns.id)
                if ns.name is not None:
                    return WordCategoryCommand(CommandQueryType.NAME, ns.name)

            if ns.command in self._rule_command_names:
                if ns.id is not None:
                    return RuleCommand(CommandQueryType.ID, ns.id)
                if ns.name is not None:
                    return RuleCommand(CommandQueryType.NAME, ns.name)
                if ns.section is not None:
                    return RuleCommand(CommandQueryType.SECTION, ns.section)
                if ns.category is not None:
                    return RuleCommand(CommandQueryType.CATEGORY, ns.category)
                if ns.summary is not None:
                    return RuleCommand(CommandQueryType.SUMMARY, ns.summary)

            if ns.command in self._save_command_names:
                if ns.name is not None:
                    return SaveCommand(ns.name)
                if ns.auto is not None and ns.auto:
                    prefix = "asdste100"
                    extension = ".svg"
                    now = datetime.now()
                    iso8601 = now.strftime("%Y-%m-%d-%H-%M-%S")
                    file_name = f"{prefix}-{iso8601}{extension}"
                    file_fullname = Path(tempfile.gettempdir()) / file_name
                    return SaveCommand(str(file_fullname))

        if ns.exit is not None:
            return ExitCommand(ns.exit)

        return UnknownCommand(text)
