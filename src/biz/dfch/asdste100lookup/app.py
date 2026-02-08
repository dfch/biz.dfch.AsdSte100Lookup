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
import random
import re

from dacite import from_dict, Config
from rich.console import Console
from rich.theme import Theme

from biz.dfch.logging import log
from biz.dfch.version import Version

from biz.dfch.asdste100vocab import Vocab
from biz.dfch.asdste100vocab import Word
from biz.dfch.asdste100vocab import WordCategory
from biz.dfch.asdste100vocab import WordNote
from biz.dfch.asdste100vocab import WordMeaning
from biz.dfch.asdste100vocab import WordStatus
from biz.dfch.asdste100vocab import WordType

from .commands.command_base import CommandBase
from .commands.empty_command import EmptyCommand
from .commands.unknown_command import UnknownCommand

from .constant import Constant
from .dictionary_files_parser import DictionaryFilesParser
from .main_prompt import MainPrompt
from .rule import Rule
from .rule_content_type import RuleContentType
from .rule_renderer import RuleRenderer


class App:  # pylint: disable=R0903
    """The application."""

    _VERSION_REQUIRED_MAJOR = 3
    _VERSION_REQUIRED_MINOR = 11

    _rule_theme = Theme(
        {
            # "markdown.h1": "bold magenta",
            # "markdown.h2": "bold cyan",
            "markdown.code": "red",
            # Not really documented. We take the definition from rich:
            # DEFAULT_STYLES: Dict[str, Style]
            # "markdown.link_url": Style(color="blue", underline=True), ...
            "markdown.link_url": "cyan",
        }
    )

    _dictionary_config = Config(
        strict=True,
        type_hooks={
            WordStatus: WordStatus,
            WordType: WordType,
            WordCategory: WordCategory,
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

        if not (
            hasattr(self._args, "no_random_word") and self._args.no_random_word
        ):
            # Display a random word at startup.
            words = [
                word
                for word in dictionary
                if word.category == WordCategory.DEFAULT
            ]
            if 0 < len(words):
                # Suppress Sonar warning. This random function is not used
                # in a security relevant context.
                word = random.choice(words)  # NOSONAR

                text = word.name
                command: CommandBase = UnknownCommand(text)
                command.invoke(console=console, dictionary=[word], rules=rules)

        while True:
            text = input(f"[{len(dictionary)}] Enter search term: ").strip()

            command = prompt.parse(text)
            command.invoke(console=console, dictionary=dictionary, rules=rules)

            if not isinstance(command, EmptyCommand):
                continue

            break

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

        # Deserialize.
        result = [
            from_dict(data_class=Rule, data=item, config=self._rules_config)
            for item in rules_json
        ]

        return result

    def on_rules(self) -> None:
        """This is the handler for the `rules` command."""

        console = Console(theme=self._rule_theme)

        current_folder = Path(__file__).parent
        rules_fullname = current_folder / Constant.RULES_FILE
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
            console=console,
            rules=selected_rules,
            type_=self._args.summary,
        )

    def _load_word_list(self, fullname: Path) -> list[Word]:

        assert isinstance(fullname, Path), type(fullname)
        assert fullname.exists(), fullname

        word_list: list[Word] = []
        with open(fullname, "r", encoding="utf-8") as f:
            for idx, line in enumerate(f, 1):
                line = line.strip()
                try:
                    item = json.loads(line)
                    word = from_dict(
                        data_class=Word,
                        data=item,
                        config=self._dictionary_config,
                    )
                    word_list.append(word)
                except Exception as ex:  # pylint: disable=W0718
                    print(f"[ERROR] {fullname}[#{idx}]: '{ex}'.")

        result = sorted(word_list, key=lambda e: e.name.lower())

        return result

    def on_dictionary(
        self,
        use_ste100: bool,
        use_technical_nouns: bool,
        use_technical_verbs: bool,
        ste100_file_name: str,
        technical_words_file_name: str,
        word_files: list[Path],
    ) -> None:
        """This is the handler for the `dictionary` command."""

        assert isinstance(use_ste100, bool)
        assert isinstance(use_technical_nouns, bool)
        assert isinstance(use_technical_verbs, bool)

        assert isinstance(ste100_file_name, str)
        assert ste100_file_name.strip()

        assert isinstance(technical_words_file_name, str)
        assert technical_words_file_name.strip()

        assert isinstance(word_files, list), type(word_files)

        log.debug("Starting to parse source data ...")

        current_folder = Path(__file__).parent

        # dictionary: list[Word] = []

        def predicate(word: Word) -> bool:
            if word.type_ == WordType.TECHNICAL_NOUN:
                return use_technical_nouns
            if word.type_ == WordType.TECHNICAL_VERB:
                return use_technical_verbs
            return True

        dictionary = Vocab(
            use_ste100=use_ste100,
            use_ste100_technical_word=use_technical_nouns
            or use_technical_verbs,
            predicate=predicate
        )

        # # Load STE dictionary.
        # if use_ste100:
        #     dictionary_fullname = current_folder / ste100_file_name
        #     dictionary = self._load_word_list(dictionary_fullname)

        # Load rules.
        rules_fullname = current_folder / Constant.RULES_FILE
        rules = self._load_rules(rules_fullname)

        # # Load technical words and add them to the dictionary.
        # if use_technical_nouns or use_technical_verbs:
        #     technical_words_fullname = (
        #         current_folder / technical_words_file_name
        #     )
        #     word_list = self._load_word_list(technical_words_fullname)

        #     # Put word list together into a single word list.
        #     if use_technical_nouns:
        #         words = [
        #             w for w in word_list if w.type_ == WordType.TECHNICAL_NOUN
        #         ]
        #         dictionary.extend(words)
        #     if use_technical_verbs:
        #         words = [
        #             w for w in word_list if w.type_ == WordType.TECHNICAL_VERB
        #         ]
        #         dictionary.extend(words)

        for word_file in word_files:
            assert word_file.exists(), str(word_file)
            print(f"Load word list '{word_file}' ...")
            word_list = self._load_word_list(word_file)
            print(f"Load word list '{word_file}' [{len(word_list)}] OK.")
            dictionary.extend(word_list)

        # Loop the resulting vocabulary alphabetically.
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
            self.on_dictionary(
                use_ste100=self._args.use_ste100,
                use_technical_nouns=self._args.use_technical_nouns,
                use_technical_verbs=self._args.use_technical_verbs,
                ste100_file_name=Constant.DICTIONARY_FILE,
                technical_words_file_name=Constant.TECHNICAL_WORDS_FILE,
                word_files=[Path(f) for f in self._args.input],
            )
            return

        self.on_dictionary(
            use_ste100=True,
            use_technical_nouns=True,
            use_technical_verbs=True,
            ste100_file_name=Constant.DICTIONARY_FILE,
            technical_words_file_name=Constant.TECHNICAL_WORDS_FILE,
            word_files=[],
        )
