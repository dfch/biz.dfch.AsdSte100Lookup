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

"""Main app module."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re

from dacite import from_dict, Config
from rich.console import Console
from rich.theme import Theme

from biz.dfch.logging import log
from biz.dfch.version import Version

from .constant import Constant
from .dictionary_files_parser import DictionaryFilesParser
from .empty_command import EmptyCommand
from .main_prompt import MainPrompt
from .rule import Rule
from .rule_content_type import RuleContentType
from .rule_renderer import RuleRenderer
from .technical_word_category import TechnicalWordCategory
from .word import Word
from .word_meaning import WordMeaning
from .word_note import WordNote
from .word_source import WordSource
from .word_status import WordStatus
from .word_type import WordType


class App:  # pylint: disable=R0903
    """The application."""

    _VERSION_REQUIRED_MAJOR = 3
    _VERSION_REQUIRED_MINOR = 11

    _rules_file_name = "rules.json"

    _rule_theme = Theme(
        {
            # "markdown.h1": "bold magenta",
            # "markdown.h2": "bold cyan",
            "markdown.code": "red",
        }
    )

    _dictionary_config = Config(
        strict=True,
        type_hooks={
            WordStatus: WordStatus,
            WordType: WordType,
            TechnicalWordCategory: TechnicalWordCategory,
        },
        forward_references={
            Word.__name__: Word,
            WordMeaning.__name__: WordMeaning,
            WordNote.__name__: WordNote,
        },
    )

    _rules_config = Config(
        strict=True,
        type_hooks={
            RuleContentType: RuleContentType,
        },
    )

    _parser: argparse.ArgumentParser
    _args: argparse.Namespace

    def __init__(self, parser: argparse.ArgumentParser):

        Version().ensure_minimum_version(
            self._VERSION_REQUIRED_MAJOR, self._VERSION_REQUIRED_MINOR
        )

        assert isinstance(parser, argparse.ArgumentParser)
        self._parser = parser
        self._args = parser.parse_args()

    def _get_technical_words_internal(
        self, rules: list[Rule], rule_id: str, prefix: str, type_: WordType
    ) -> list[Word]:
        """Returns all technical nouns from rule R1.5."""

        assert isinstance(rules, list)
        for rule in rules:
            assert isinstance(rule, Rule)

        result: list[Word] = []

        rule = next((r for r in rules if r.id_ == rule_id))
        assert isinstance(rule, Rule)

        current_category: str = ""
        contents = [d for d in rule.contents if d.type_ in ("text", "good")]
        for content in contents:
            if RuleContentType.TEXT == content.type_:
                match = re.match(r"^(?P<category>\d+)\.", content.data.strip())
                if not match:
                    continue
                current_category = f"{prefix}{match.group('category')}"
                continue

            category_word_list = content.data.split(", ")
            for category_word in category_word_list:
                note = WordNote(
                    value=f"See '{WordSource.STE100_9}' ({current_category})."
                )
                word = Word(
                    status=WordStatus.CUSTOM,
                    source=WordSource.STE100_9,
                    category=TechnicalWordCategory(current_category),
                    name=category_word.strip(),
                    type_=type_,
                    meanings=[],
                    spellings=[],
                    alternatives=[],
                    ste_example=[],
                    nonste_example=[],
                    note=note,
                )
                result.append(word)

        return result

    def _get_technical_words(self, rules: list[Rule]) -> list[Word]:
        """Returns all technical nouns and verbs from rules R1.5 and R1.12."""

        assert isinstance(rules, list)

        result: list[Word] = []

        result = self._get_technical_words_internal(
            rules,
            rule_id="R1.5",
            prefix="TN",
            type_=WordType.TECHNICAL_NOUN
        )

        result.extend(
            self._get_technical_words_internal(
                rules,
                rule_id="R1.12",
                prefix="TV",
                type_=WordType.TECHNICAL_VERB
            )
        )

        return result

    def prompt_user_loop(
        self,
        dictionary: list[Word],
        rules: list[Rule],
    ) -> None:
        """Main program loop."""

        assert isinstance(dictionary, list)
        for item in dictionary:
            assert isinstance(item, Word)

        prompt = MainPrompt()
        console = Console(theme=self._rule_theme, record=True)

        while True:
            text = input(f"[{len(dictionary)}] Enter search term: ").strip()

            command = prompt.parse(text)
            command.invoke(console=console, dictionary=dictionary, rules=rules)

            if not isinstance(command, EmptyCommand):
                continue

            log.debug("Exiting ...")
            break

    # @staticmethod
    # def extract_ste_nonste(line_info: LineInfo) -> tuple[str, str] | None:
    #     """Extracts ste and non ste examples from LineInfo."""
    #     assert line_info is not None

    #     tokens = line_info.tokens

    #     if line_info.tokens_count <= ColumnIndex.MEANING_ALT:
    #         return None

    #     ste_example = ""
    #     if line_info.tokens_count > ColumnIndex.STE:
    #         ste_example = tokens[ColumnIndex.STE]

    #     nonste_example = ""
    #     if line_info.tokens_count > ColumnIndex.NONSTE:
    #         nonste_example = tokens[ColumnIndex.NONSTE]

    #     return (ste_example.strip(), nonste_example.strip())

    # @staticmethod
    # def extract_word(line_info: LineInfo) -> Word | None:
    #     """Extracts a Word from LineInfo."""

    #     assert line_info is not None

    #     tokens = line_info.tokens

    #     if line_info.tokens_count <= ColumnIndex.MEANING_ALT:
    #         return None

    #     meaning_or_alt = tokens[ColumnIndex.MEANING_ALT].strip()

    #     dict_word = DictionaryInfo.get_single_word(meaning_or_alt)
    #     if not dict_word:
    #         return None

    #     ste_example = ""
    #     if line_info.tokens_count > ColumnIndex.STE:
    #         ste_example = tokens[ColumnIndex.STE]

    #     nonste_example = ""
    #     if line_info.tokens_count > ColumnIndex.NONSTE:
    #         nonste_example = tokens[ColumnIndex.NONSTE]

    #     result = Word(
    #         status=dict_word.status,
    #         name=dict_word.name,
    #         type_=dict_word.type_,
    #         source=WordSource.STE100_9,
    #         meanings=[],
    #         spellings=[],
    #         alternatives=[],
    #         ste_example=[ste_example],
    #         nonste_example=[nonste_example],
    #     )
    #     return result

    def on_parse(self) -> None:
        """This is the handler for the `dictionary` command."""

        # How elegant!
        root_dir = Path(__file__).resolve().parent.parent.parent.parent.parent
        import_path = self._args.path
        path = root_dir.joinpath(import_path)
        prefix = self._args.prefix
        extension = self._args.extension
        dictionary_file_name = self._args.output
        DictionaryFilesParser().invoke(
            path=path,
            prefix=prefix,
            extension=extension,
            dictionary_file_name=dictionary_file_name,
        )

    def _load_rules(self, file_path_and_name: Path) -> list[Rule]:
        """Loads rules from file."""

        assert isinstance(file_path_and_name, Path)

        # Load rules file.
        with open(file_path_and_name, "r", encoding="utf-8") as f:
            rules_json = json.load(f)

        # Deserialise.
        result = [
            from_dict(data_class=Rule, data=item, config=self._rules_config)
            for item in rules_json
        ]

        return result

    def on_rules(self) -> None:
        """This is the handler for the `rules` command."""

        console = Console(theme=self._rule_theme)

        current_folder = Path(__file__).parent
        rules_fullname = current_folder / self._rules_file_name
        rules = self._load_rules(rules_fullname)

        selected_rules: list[Rule] = []
        for rule in rules:

            if self._args.list:
                selected_rules.append(rule)
                continue

            if self._args.id:
                if re.search(self._args.id, rule.id_, re.IGNORECASE):
                    selected_rules.append(rule)
                    continue

            if self._args.section:
                if re.search(self._args.section, rule.section, re.IGNORECASE):
                    selected_rules.append(rule)
                    continue

            if self._args.category:
                if re.search(self._args.category, rule.category, re.IGNORECASE):
                    selected_rules.append(rule)
                    continue

        RuleRenderer().show(
            console=console, rules=selected_rules, is_summary_only=self._args.summary
        )

    def on_dictionary(self, dictionary_file_name: str) -> None:
        """This is the handler for the `dictionary` command."""

        assert (
            isinstance(dictionary_file_name, str) and "" != dictionary_file_name.strip()
        )

        assert dictionary_file_name is not None and "" != dictionary_file_name

        log.debug("Starting to parse source data ...")

        current_folder = Path(__file__).parent

        # Load STE dictionary.
        dictionary_fullname = current_folder / dictionary_file_name
        with open(dictionary_fullname, "r", encoding="utf-8") as f:
            dictionary_json = json.load(f)

        word_list = [
            from_dict(data_class=Word, data=item, config=self._dictionary_config)
            for item in dictionary_json
        ]
        dictionary = sorted(word_list, key=lambda e: e.name.lower())

        # Load rules.
        rules_fullname = current_folder / self._rules_file_name
        rules = self._load_rules(rules_fullname)

        # Load technical words and add them to the ditionary.
        techncal_words = self._get_technical_words(rules)
        dictionary.extend(techncal_words)
        dictionary = sorted(dictionary, key=lambda e: e.name.lower())

        self.prompt_user_loop(dictionary=dictionary, rules=rules)

    def invoke(self) -> None:
        """Main entry point for this class."""

        # Set the effective log level.
        from .args import Args  # pylint: disable=C0415

        log_level = Args.get_effective_log_level_name(self._args)
        import logging  # pylint: disable=C0415

        for handler in logging.getLogger().handlers:
            handler.setLevel(log_level)

        # Print program information.
        log.debug(self._parser.description)
        print(self._parser.description)
        log.debug(self._parser.epilog)
        print(self._parser.epilog)

        if self._args.command == "parse":
            self.on_parse()
            return

        if self._args.command == "rules":
            self.on_rules()
            return

        if self._args.command == "dictionary":
            self.on_dictionary(self._args.input)
            return

        self.on_dictionary(Constant.DICTIONARY_FILE)
