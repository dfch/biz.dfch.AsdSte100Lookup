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
from .commands.filter_command import FilterCommand
from .commands.help_command import HelpCommand
from .commands.rule_command import RuleCommand
from .commands.save_command import SaveCommand
from .commands.sentence_info_command import SentenceInfoCommand
from .commands.unknown_command import UnknownCommand
from .commands.word_category_command import WordCategoryCommand
from .commands.word_filter_type import WordFilterType
from .rule_render_type import RuleRenderType

from .word_category import WordCategory
from .word_type import WordType
from .word_status import WordStatus


class MainPrompt:  # pylint: disable=R0903
    """Represents the main prompt processing."""

    _start_of_command: str = "!"

    _help_command_names = ["?", "-h", "--help"]
    _category_command_names = ["category", "c"]
    _rule_command_names = ["rule", "r"]
    _save_command_names = ["save", "s"]
    _exit_command_names = ["exit", "x"]
    _filter_command_names = ["filter", "f"]
    _sentence_command_names = ["sentence", "1"]

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
            "(eg. '! exit').",
            add_help=True,
        )

        subparsers_action = result.add_subparsers(
            dest="command", required=True, help="Available commands."
        )

        self._build_parser_category(subparsers_action)
        self._build_parser_rule(subparsers_action)
        self._build_parser_save(subparsers_action)
        self._build_parser_exit(subparsers_action)
        self._build_parser_filter(subparsers_action)
        self._build_parser_sentence(subparsers_action)

        return result

    def _build_parser_category(
        self, subparsers_action
    ) -> SuppressErrorMessageArgumentParser:
        parser = subparsers_action.add_parser(
            self._category_command_names[0],
            aliases=self._category_command_names[1:],
            help="This command shows all words from the specified category.",
        )

        result = parser.add_mutually_exclusive_group(required=True)
        result.add_argument(
            "-i",
            "--id",
            help="Id (short name) of the word category to query.",
        )

        result.add_argument(
            "-n",
            "--name",
            help="Name of the word category to query.",
        )

        result.add_argument(
            "-l",
            "--list",
            action="store_true",
            help="List the ids and category names.",
        )

        return result

    def _build_parser_rule(
        self, subparsers_action
    ) -> SuppressErrorMessageArgumentParser:
        parser = subparsers_action.add_parser(
            self._rule_command_names[0],
            aliases=self._rule_command_names[1:],
            help="This command shows the specified rule.",
        )

        result = parser.add_mutually_exclusive_group(required=True)
        result.add_argument(
            "-i",
            "--id",
            help="Id of the rule to query.",
        )

        result.add_argument(
            "-n",
            "--name",
            help="Name of the rule to query.",
        )

        result.add_argument(
            "-s",
            "--section",
            help="Section of the rule to query.",
        )

        result.add_argument(
            "-c",
            "--category",
            help="Category of the rule to query.",
        )

        result.add_argument(
            "--summary",
            help="Summary of the rule to query.",
        )

        result.add_argument(
            "-t",
            "--text",
            help="Text of the rule to query.",
        )

        result.add_argument(
            "-a",
            "--all",
            action="store_true",
            help="Overview of all rules.",
        )

        rule_parser_output_args = parser.add_mutually_exclusive_group(
            required=False
        )

        rule_parser_output_args.add_argument(
            "-l",
            "--list",
            action="store_true",
            help="List the id and name of the matching rules.",
        )

        rule_parser_output_args.add_argument(
            "-b",
            "--brief",
            action="store_true",
            help="List a brief overview of the matching rules.",
        )

        return result

    def _build_parser_save(
        self, subparsers_action
    ) -> SuppressErrorMessageArgumentParser:
        parser = subparsers_action.add_parser(
            self._save_command_names[0],
            aliases=self._save_command_names[1:],
            help="This command writes the last console output to a file.",
        )

        result = parser.add_mutually_exclusive_group(required=True)

        result.add_argument(
            "-n",
            "--name",
            help="Give the name of the file.",
        )

        result.add_argument(
            "-a",
            "--auto",
            action="store_true",
            help="Automatically select a unique name for the file.",
        )

        return result

    def _build_parser_exit(
        self, subparsers_action
    ) -> SuppressErrorMessageArgumentParser:
        result = subparsers_action.add_parser(
            self._exit_command_names[0],
            aliases=self._exit_command_names[1:],
            help="This command stops the programme.",
        )

        return result

    def _build_parser_filter(
        self, subparsers_action
    ) -> SuppressErrorMessageArgumentParser:
        parser = subparsers_action.add_parser(
            self._filter_command_names[0],
            aliases=self._filter_command_names[1:],
            help="Modifies the filter for dictionary queries.",
        )

        result = parser.add_mutually_exclusive_group(required=True)

        result.add_argument(
            "-l",
            "--list",
            action="store_true",
            help="Show all filters.",
        )

        result.add_argument(
            "-r",
            "--reset",
            action="store_true",
            help="Resets all filters.",
        )

        result.add_argument(
            "-t",
            "--type",
            "--word_type",
            metavar="TYPE",
            type=lambda s: s.lower(),
            choices=[item.value.lower() for item in WordType],
            help="Sets the filter for word type. "
            f"{[item.value.lower() for item in WordType]}.",
        )

        result.add_argument(
            "-s",
            "--status",
            metavar="STATUS",
            type=lambda s: s.lower(),
            choices=[item.value.lower() for item in WordStatus],
            help="Sets the filter for word status: "
            f"{[item.value.lower() for item in WordStatus]}.",
        )

        result.add_argument(
            "-src",
            "--source",
            type=str,
            help="Sets the filter for word source.",
        )

        result.add_argument(
            "-c",
            "--category",
            metavar="CAT",
            type=lambda s: s.lower(),
            choices=[item.value.lower() for item in WordCategory],
            help="Sets the filter for word category: "
            f"{[item.value.lower() for item in WordCategory]}.",
        )

        result.add_argument(
            "-n",
            "--note",
            type=str,
            help="Sets the filter for words with a note.",
        )

        return result

    def _build_parser_sentence(
        self, subparsers_action
    ) -> SuppressErrorMessageArgumentParser:
        result = subparsers_action.add_parser(
            self._sentence_command_names[0],
            aliases=self._sentence_command_names[1:],
            help="Analyses a sentence.",
        )
        result.add_argument(
            "text", nargs="*", help="The sentence text to analyze"
        )
        sentence_parser_args = result.add_mutually_exclusive_group(
            required=True
        )
        sentence_parser_args.add_argument(
            "-i", "--info", action="store_true", help="Shows info."
        )
        sentence_parser_args.add_argument(
            "-c", "--count", action="store_true", help="Shows word count."
        )

        return result

    def parse(self, text: str) -> CommandBase:
        """Parses a line of text into a command."""

        if not isinstance(text, str) or "" == text.strip():
            return EmptyCommand("")

        text = text.strip()

        if text in self._help_command_names:
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
        # the dictionary.
        # This is intended.
        except SystemExit as ex:  # NOSONAR
            if "0" == str(ex):
                return HelpCommand("")

            return HelpCommand(self._parser.format_help())

        if ns.command is None:
            return UnknownCommand(text)

        if ns.command in self._category_command_names:
            return self._parse_category(ns)

        if ns.command in self._rule_command_names:
            return self._parse_rule(ns)

        if ns.command in self._save_command_names:
            return self._parse_save(ns)

        if ns.command in self._filter_command_names:
            return self._parse_filter(ns)

        if ns.command in self._sentence_command_names:
            return self._parse_sentence(ns)

        if ns.command in self._exit_command_names:
            return ExitCommand(ns.command)

        return UnknownCommand(text)

    def _parse_category(self, ns) -> CommandBase:
        if ns.list is not None and True is ns.list:
            return WordCategoryCommand(CommandQueryType.LIST, "")
        if ns.id is not None:
            return WordCategoryCommand(CommandQueryType.ID, ns.id)
        if ns.name is not None:
            return WordCategoryCommand(CommandQueryType.NAME, ns.name)

        raise ValueError("Invalid command option (category).")

    def _parse_rule(self, ns) -> CommandBase:
        display_type = RuleRenderType.DEFAULT
        if ns.list is not None and True is ns.list:
            display_type = RuleRenderType.LIST
        if ns.brief is not None and True is ns.brief:
            display_type = RuleRenderType.BRIEF

        if ns.id is not None:
            return RuleCommand(
                CommandQueryType.ID, ns.id, display_type=display_type
            )
        if ns.name is not None:
            return RuleCommand(
                CommandQueryType.NAME, ns.name, display_type=display_type
            )
        if ns.section is not None:
            return RuleCommand(
                CommandQueryType.SECTION,
                ns.section,
                display_type=display_type,
            )
        if ns.category is not None:
            return RuleCommand(
                CommandQueryType.CATEGORY,
                ns.category,
                display_type=display_type,
            )
        if ns.summary is not None:
            return RuleCommand(
                CommandQueryType.SUMMARY,
                ns.summary,
                display_type=display_type,
            )
        if ns.text is not None:
            return RuleCommand(
                CommandQueryType.TEXT,
                ns.text,
                display_type=display_type,
            )
        if ns.all is not None:
            return RuleCommand(
                CommandQueryType.ALL,
                "",
                display_type=RuleRenderType.LIST,
            )

        raise ValueError("Invalid command option (rule).")

    def _parse_save(self, ns) -> CommandBase:
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

        raise ValueError("Invalid command option (save).")

    def _parse_filter(self, ns) -> CommandBase:
        if ns.reset is not None and ns.reset:
            return FilterCommand(WordFilterType.RESET, "")
        if ns.list is not None and ns.list:
            return FilterCommand(WordFilterType.LIST, "")
        if ns.type is not None:
            return FilterCommand(WordFilterType.TYPE, ns.type)
        if ns.status is not None:
            return FilterCommand(WordFilterType.STATUS, ns.status)
        if ns.category is not None:
            return FilterCommand(WordFilterType.CATEGORY, ns.category)
        if ns.source is not None:
            return FilterCommand(WordFilterType.SOURCE, ns.source)
        if ns.note is not None:
            return FilterCommand(WordFilterType.NOTE, ns.note)

        raise ValueError("Invalid command option (filter).")

    def _parse_sentence(self, ns) -> CommandBase:
        if ns.count is not None and ns.count:
            _ = True
        if ns.info is not None and ns.info:
            _ = True
        text = ""
        if ns.text is not None:
            text = " ".join(ns.text)

        return SentenceInfoCommand(text)
