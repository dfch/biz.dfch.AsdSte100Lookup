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
from dataclasses import asdict
from itertools import zip_longest
import json
from pathlib import Path
import re
from typing import cast

from dacite import from_dict, Config
from rich import box
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.table import Table
from rich.theme import Theme

# from biz.dfch.i18n import LanguageCode
from biz.dfch.logging import log
from biz.dfch.version import Version

from .column_index import ColumnIndex
from .colouriser import Colouriser
from .dictionary_info import DictionaryInfo
from .line_info import LineInfo
from .line_info_type import LineInfoType
from .markdown_utils import MarkDownUtils
from .rule import Rule
from .rule_content_type import RuleContentType
from .table_row import TableRow
from .technical_word_category import TechnicalWordCategory
from .word import Word
from .word_info import WordInfo
from .word_meaning import WordMeaning
from .word_note import WordNote
from .word_source import WordSource
from .word_state import WordState
from .word_status import WordStatus
from .word_type import WordType


class App:  # pylint: disable=R0903
    """The application."""

    _VERSION_REQUIRED_MAJOR = 3
    _VERSION_REQUIRED_MINOR = 11

    _rules_file_name = "rules.json"

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

    def to_colour(self, text: str, value: str, status: str) -> str:
        """Colourises value in specified text green or red based on status."""
        if WordStatus.APPROVED == status:
            result = Colouriser(text).to_green(value)
        elif WordStatus.CUSTOM == status:
            result = Colouriser(text).to_darkergreen(value)
        else:
            result = Colouriser(text).to_red(value)

        return result

    def _get_first_or_item(self, item: str | list[str] | None) -> str | None:
        """
        Retrieves the first `item` of a list or the `item` itself.
        If `item` is `None` or the list is empty, `None` is returned.

        Args:
            item (str | list[str] | None): A list of strings or a string.

        Returns:
            (str | None): - The first `item` in the list, if it is a list
                - The `item`, if it is not a list
                - None, if `item` or the list is empty.
        """

        if item is None:
            return None

        if isinstance(item, list):
            return item[0] if item else None

        return item

    def _get_technical_words_internal(
            self,
            rules: list[Rule],
            rule_id: str,
            prefix: str,
            type_: WordType
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
                match = re.match(r'^(?P<category>\d+)\.', content.data.strip())
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

    def _get_technical_words(self) -> list[Word]:
        """Returns all technical nouns and verbs from rules R1.5 and R1.12."""

        result: list[Word] = []

        current_folder = Path(__file__).parent
        rules_fullname = current_folder / self._rules_file_name
        rules = self._load_rules(rules_fullname)

        result = self._get_technical_words_internal(
            rules,
            rule_id="R1.5",
            prefix="TN",
            type_=WordType.TECHNICAL_NOUN)

        result.extend(self._get_technical_words_internal(
            rules,
            rule_id="R1.12",
            prefix="TV",
            type_=WordType.TECHNICAL_VERB))

        return result

#     def prompt_show_help(self, console: Console) -> None:
#         """Shows the help text."""

#         assert isinstance(console, Console)
    
#         console.print(f"""?   This help text.
# category:
# """)

    def prompt_user_loop(self, dictionary: list[Word]) -> None:
        """Main program loop."""

        assert isinstance(dictionary, list)
        for item in dictionary:
            assert isinstance(item, Word)

        console = Console()
        while True:
            prompt = input(f"[{len(dictionary)}] Enter search term: ").strip()
            if prompt is None or "" == prompt:
                log.debug("Exiting ...")
                break

            # Create the table
            table = Table()
            table.add_column("Word", no_wrap=True, min_width=16)
            table.add_column("Meaning/ALTERNATIVE", min_width=16)
            table.add_column("STE Example")
            table.add_column("Non-STE Example")

            matching_words: dict[int, Word] = {}
            try:
                for word in dictionary:
                    if re.search(prompt, word.name, re.IGNORECASE):
                        matching_words[id(word)] = word
                        continue

                    for spelling in word.spellings:
                        if re.search(prompt, spelling, re.IGNORECASE):
                            matching_words[id(word)] = word
                            continue

                    if self._get_first_or_item(word.ste_example) and re.search(
                        prompt,
                        cast(str, self._get_first_or_item(word.ste_example)),
                        re.IGNORECASE,
                    ):
                        matching_words[id(word)] = word
                        continue

                    if self._get_first_or_item(word.nonste_example) and re.search(
                        prompt,
                        cast(str, self._get_first_or_item(word.nonste_example)),
                        re.IGNORECASE,
                    ):
                        matching_words[id(word)] = word
                        continue

            except re.error as ex:
                log.error("Invalid regex: '%s'", ex)

            rows: list[TableRow] = []
            for word in matching_words.values():

                row = TableRow()
                rows.append(row)

                if WordStatus.APPROVED == word.status:
                    if word.name:
                        row.word = self.to_colour(
                            f"{word.name.upper()} ({word.type_})",
                            word.name,
                            word.status,
                        )
                    if self._get_first_or_item(word.ste_example):
                        row.ste_example = self.to_colour(
                            cast(str, self._get_first_or_item(word.ste_example)),
                            prompt,
                            word.status,
                        )
                elif WordStatus.REJECTED == word.status:
                    if word.name:
                        row.word = self.to_colour(
                            f"{word.name.lower()} ({word.type_})",
                            word.name,
                            word.status,
                        )
                    if self._get_first_or_item(word.nonste_example):
                        row.nonste_example = self.to_colour(
                            cast(str, self._get_first_or_item(word.nonste_example)),
                            prompt,
                            word.status,
                        )
                elif WordStatus.CUSTOM == word.status:
                    if word.name:
                        row.word = self.to_colour(
                            f"{word.name.upper()} ({word.type_})",
                            word.name,
                            word.status,
                        )
                    if self._get_first_or_item(word.ste_example):
                        row.ste_example = self.to_colour(
                            cast(str, self._get_first_or_item(word.ste_example)),
                            prompt,
                            word.status,
                        )
                else:
                    log.error(f"Word '{word.name} with status '{word.status}' found.")
                    continue

                if word.spellings:
                    colourised_spellings: list[str] = [
                        str(Colouriser(x, "blue")) for x in word.spellings
                    ]

                    spellings = "\n".join(colourised_spellings)
                    row.word = f"{row.word}\n{spellings}"

                if word.meanings:
                    meanings = word.meanings
                    for meaning in meanings:
                        if row.ste_example or row.nonste_example:
                            row = TableRow()
                            rows.append(row)
                        row.description = meaning.value
                        if meaning.ste_example:
                            row.ste_example = self.to_colour(
                                meaning.ste_example, word.name, word.status
                            )
                        if meaning.nonste_example:
                            row.nonste_example = self.to_colour(
                                meaning.nonste_example, word.name, WordStatus.REJECTED
                            )

                if word.alternatives:
                    alternatives = word.alternatives
                    for alt in alternatives:
                        if row.description:
                            row = TableRow()
                            rows.append(row)

                        row.description = self.to_colour(
                            f"{alt.name.upper()} ({alt.type_})", alt.name, alt.status
                        )

                        # Process examples pairwise.
                        ste_list = (
                            alt.ste_example
                            if isinstance(alt.ste_example, list)
                            else ([] if alt.ste_example is None else [alt.ste_example])
                        )
                        nonste_list = (
                            alt.nonste_example
                            if isinstance(alt.nonste_example, list)
                            else (
                                []
                                if alt.nonste_example is None
                                else [alt.nonste_example]
                            )
                        )
                        for i, (ste, nonste) in enumerate(
                            zip_longest(ste_list, nonste_list, fillvalue=" ")
                        ):

                            if 0 == i:
                                row.ste_example = self.to_colour(
                                    ste, alt.name, alt.status
                                )
                                row.nonste_example = self.to_colour(
                                    nonste, word.name, WordStatus.REJECTED
                                )
                                continue

                            row = TableRow()
                            rows.append(row)

                            row.ste_example = self.to_colour(ste, alt.name, alt.status)
                            row.nonste_example = self.to_colour(
                                nonste, word.name, WordStatus.REJECTED
                            )

                if word.note:
                    if isinstance(word.note, WordNote):
                        note = word.note
                    else:
                        note = word.note

                    if note.words:
                        nwords = note.words

                        if row.description or row.ste_example or row.nonste_example:

                            row = TableRow()
                            rows.append(row)

                        row.description = str(Colouriser(note.value, "yellow"))

                        for nword in nwords:
                            row = TableRow()
                            rows.append(row)
                            row.description = self.to_colour(
                                f"{nword.name} ({nword.type_})",
                                nword.name,
                                nword.status,
                            )
                            if self._get_first_or_item(nword.ste_example):
                                row.ste_example = self.to_colour(
                                    cast(
                                        str, self._get_first_or_item(nword.ste_example)
                                    ),
                                    nword.name,
                                    WordStatus.APPROVED,
                                )
                            if self._get_first_or_item(nword.nonste_example):
                                row.nonste_example = self.to_colour(
                                    cast(
                                        str,
                                        self._get_first_or_item(nword.nonste_example),
                                    ),
                                    nword.name,
                                    WordStatus.REJECTED,
                                )
                    elif note.value:
                        row = TableRow()
                        row.description = str(Colouriser(note.value, "yellow"))
                        if note.ste_example:
                            row.ste_example = self.to_colour(
                                note.ste_example, word.name, WordStatus.APPROVED
                            )
                        if note.nonste_example:
                            row.nonste_example = self.to_colour(
                                note.nonste_example, word.name, WordStatus.REJECTED
                            )
                        rows.append(row)

                rows.append(TableRow())

            if rows:
                for row in rows:
                    if row.description:
                        row.description = row.description.replace("\u200b", "")
                    log.debug(
                        f"'{row.word}', '{row.description}', "
                        f"'{row.ste_example}', "
                        f"'{row.nonste_example}'"
                    )
                    table.add_row(
                        row.word or "",
                        row.description or "",
                        row.ste_example or "",
                        row.nonste_example or "",
                    )
                console.print(table)

    def process_file(self, file: Path) -> tuple[list[LineInfo], list[WordInfo]]:
        """Parses a single OCR dictionary file."""

        assert file is not None and isinstance(file, Path)

        log.debug("Processing file '%s' ...", file.name)

        lines: list[str] = []
        with open(file, "r", encoding="utf-8") as f:

            for line in f:
                if not line:
                    continue

                lines.append(line)

        line_infos: list[LineInfo] = []
        word_infos: list[WordInfo] = []
        result: tuple[list[LineInfo], list[WordInfo]] = (line_infos, word_infos)

        if not lines:
            log.warning(
                "Processing file '%s' FAILED. "
                "File does not contain text. "
                "Skipping file.",
                file.name,
            )
            return result

        for line in lines:
            line_info = LineInfo()
            line_info.line = line.strip("\ufeff")
            line_info.tokens = line_info.line.split("\t")
            line_info.tokens_count = len(line_info.tokens)
            if not line_info.tokens:
                continue

            token = line_info.tokens[0]
            if DictionaryInfo.is_word(token):
                line_info.is_start_of_word = True

            log.debug(
                "[%s] [%s] %s",
                line_info.tokens_count,
                line_info.is_start_of_word,
                line_info.line,
            )

            # for index, token in enumerate(line_info.tokens):
            #     log.debug("[%s/%s] '%s'", index, line_info.tokens_count, token)

            line_infos.append(line_info)

        word_info: WordInfo = WordInfo(file.name)
        for index, line_info in enumerate(line_infos):
            # log.debug("[%s] [%s] '%s'", word_info.filename, index, line_info.line)
            if 0 == index:
                assert line_info.is_start_of_word

            if line_info.is_start_of_word:
                word_info = WordInfo(file.name)
                word = DictionaryInfo.get_word(line_info.tokens[0])
                assert word is not None
                assert WordStatus.UNKNOWN != word.status

                word_info.word = word
                word_infos.append(word_info)

            word_info.line_infos.append(line_info)

        for word_info in word_infos:
            # log.debug("%s", word_info.line_infos[0].tokens[0])
            log.debug(
                "'%s' [%s] %s [#%s]",
                word_info.word.name,
                word_info.word.type_,
                word_info.word.status,
                len(word_info.line_infos),
            )

        # log.info("Processing file '%s' SUCCEEDED.", file.name)

        return result

    def extract_ste_nonste(self, line_info: LineInfo) -> tuple[str, str] | None:
        """Extracts ste and non ste examples from LineInfo."""
        assert line_info is not None

        tokens = line_info.tokens

        if line_info.tokens_count <= ColumnIndex.MEANING_ALT:
            return None

        ste_example = ""
        if line_info.tokens_count > ColumnIndex.STE:
            ste_example = tokens[ColumnIndex.STE]

        nonste_example = ""
        if line_info.tokens_count > ColumnIndex.NONSTE:
            nonste_example = tokens[ColumnIndex.NONSTE]

        return (ste_example.strip(), nonste_example.strip())

    def extract_word(self, line_info: LineInfo) -> Word | None:
        """Extracts a Word from LineInfo."""

        assert line_info is not None

        tokens = line_info.tokens

        if line_info.tokens_count <= ColumnIndex.MEANING_ALT:
            return None

        meaning_or_alt = tokens[ColumnIndex.MEANING_ALT].strip()

        dict_word = DictionaryInfo.get_single_word(meaning_or_alt)
        if not dict_word:
            return None

        ste_example = ""
        if line_info.tokens_count > ColumnIndex.STE:
            ste_example = tokens[ColumnIndex.STE]

        nonste_example = ""
        if line_info.tokens_count > ColumnIndex.NONSTE:
            nonste_example = tokens[ColumnIndex.NONSTE]

        result = Word(
            status=dict_word.status,
            name=dict_word.name,
            type_=dict_word.type_,
            source=WordSource.STE100_9,
            meanings=[],
            spellings=[],
            alternatives=[],
            ste_example=[ste_example],
            nonste_example=[nonste_example],
        )
        return result

    def get_next_state(
        self, current_state: WordState, line_info: LineInfo
    ) -> WordState:
        """Returns the next state based on the current state and line_info."""

        assert line_info is not None

        next_state: WordState = WordState.ERROR
        line_info_type = line_info.get_type()

        if WordState.INITIAL == current_state:
            if LineInfoType.MEANING == line_info_type:
                return WordState.WORD_MEANING
            if LineInfoType.ALTERNATIVE == line_info_type:
                return WordState.WORD_ALTERNATIVE
            if LineInfoType.NOTE == line_info_type:
                return WordState.WORD_NOTE

        if WordState.WORD_MEANING == current_state:
            if LineInfoType.MEANING == line_info_type:
                return WordState.MEANING
            if LineInfoType.EXAMPLE == line_info_type:
                return WordState.MEANING_EXAMPLE
            if LineInfoType.NOTE == line_info_type:
                return WordState.NOTE
        if WordState.WORD_ALTERNATIVE == current_state:
            if LineInfoType.ALTERNATIVE == line_info_type:
                return WordState.ALTERNATIVE
            if LineInfoType.EXAMPLE == line_info_type:
                return WordState.ALTERNATIVE_EXAMPLE
            if LineInfoType.NOTE == line_info_type:
                return WordState.NOTE
        if WordState.WORD_NOTE == current_state:
            return WordState.ERROR

        if WordState.MEANING == current_state:
            if LineInfoType.MEANING == line_info_type:
                return WordState.MEANING
            if LineInfoType.EXAMPLE == line_info_type:
                return WordState.MEANING_EXAMPLE
            if LineInfoType.NOTE == line_info_type:
                return WordState.NOTE
        if WordState.MEANING_EXAMPLE == current_state:
            if LineInfoType.MEANING == line_info_type:
                return WordState.MEANING
            if LineInfoType.EXAMPLE == line_info_type:
                return WordState.MEANING_EXAMPLE
            if LineInfoType.NOTE == line_info_type:
                return WordState.NOTE
        if WordState.ALTERNATIVE == current_state:
            if LineInfoType.ALTERNATIVE == line_info_type:
                return WordState.ALTERNATIVE
            if LineInfoType.EXAMPLE == line_info_type:
                return WordState.ALTERNATIVE_EXAMPLE
            if LineInfoType.NOTE == line_info_type:
                return WordState.NOTE
        if WordState.ALTERNATIVE_EXAMPLE == current_state:
            if LineInfoType.ALTERNATIVE == line_info_type:
                return WordState.ALTERNATIVE
            if LineInfoType.EXAMPLE == line_info_type:
                return WordState.ALTERNATIVE_EXAMPLE
            if LineInfoType.NOTE == line_info_type:
                return WordState.NOTE

        if WordState.NOTE == current_state:
            if LineInfoType.ALTERNATIVE == line_info_type:
                return WordState.NOTE_ALTERNATIVE
        if WordState.NOTE_ALTERNATIVE == current_state:
            if LineInfoType.ALTERNATIVE == line_info_type:
                return WordState.NOTE_ALTERNATIVE
            if LineInfoType.EXAMPLE == line_info_type:
                return WordState.NOTE_ALTERNATIVE_EXAMPLE
        if WordState.NOTE_ALTERNATIVE_EXAMPLE == current_state:
            if LineInfoType.ALTERNATIVE == line_info_type:
                return WordState.NOTE_ALTERNATIVE

        return next_state

    def process_wordinfo(self, item: WordInfo) -> Word | None:
        """Processes a WordInfo."""

        assert item is not None

        # Process first line_info.
        current_state = WordState.INITIAL
        assert 0 < len(item.line_infos)
        line_info = item.line_infos[0]
        next_state = self.get_next_state(current_state, line_info)
        log.debug(
            f"[{item.filename}] [{current_state.name} --> {next_state.name}] @ "
            f"{line_info.get_type().name}: {line_info.line}"
        )
        assert WordState.ERROR != next_state
        previous_state = current_state
        current_state = next_state

        name = line_info.get_name()
        assert name
        description = line_info.get_description()
        assert description
        ste = line_info.get_ste()
        non_ste = line_info.get_nonste()
        spellings = DictionaryInfo.get_spellings(name)

        match current_state:
            case WordState.WORD_MEANING:
                meanning = WordMeaning(
                    value=description,
                    ste_example=ste or "",
                    nonste_example=non_ste or "",
                )
                xyz = Word(
                    status=item.word.status,
                    name=item.word.name,
                    type_=item.word.type_,
                    source=WordSource.STE100_9,
                    meanings=[meanning],
                    spellings=spellings,
                    alternatives=[],
                    note=WordNote(value=""),
                )
            case WordState.WORD_ALTERNATIVE:
                alt_word = DictionaryInfo.get_single_word(description)
                assert alt_word
                alternative = Word(
                    status=alt_word.status,
                    name=alt_word.name,
                    type_=alt_word.type_,
                    source=WordSource.STE100_9,
                    meanings=[],
                    spellings=[],
                    alternatives=[],
                    ste_example=[],
                    nonste_example=[],
                )
                if ste:
                    alternative.ste_example.append(ste)
                if non_ste:
                    alternative.nonste_example.append(non_ste)
                xyz = Word(
                    status=item.word.status,
                    name=item.word.name,
                    type_=item.word.type_,
                    source=WordSource.STE100_9,
                    meanings=[],
                    spellings=spellings,
                    alternatives=[alternative],
                    note=WordNote(value=""),
                )
            case WordState.WORD_NOTE:
                xyz = Word(
                    status=item.word.status,
                    name=item.word.name,
                    type_=item.word.type_,
                    source=WordSource.STE100_9,
                    meanings=[],
                    spellings=spellings,
                    alternatives=[],
                    note=WordNote(
                        value=DictionaryInfo.get_note(description),
                        ste_example=ste or "",
                        nonste_example=non_ste or "",
                    ),
                )
            case _:
                raise ValueError(
                    f"[{previous_state}] --> [{current_state}] "
                    f"@ {line_info.get_type().name}: '{line_info}'"
                )
        assert xyz

        for line_info in item.line_infos[1:]:
            next_state = self.get_next_state(current_state, line_info)
            log.debug(
                f"[{item.filename}] "
                f"[{current_state.name} --> {next_state.name}] "
                f"@ {line_info.get_type().name}: {line_info.line}"
            )
            assert WordState.ERROR != next_state
            previous_state = current_state
            current_state = next_state

            description = line_info.get_description()
            ste = line_info.get_ste()
            non_ste = line_info.get_nonste()
            match current_state:
                case WordState.NOTE:
                    assert description
                    assert xyz.note
                    xyz.note.value = DictionaryInfo.get_note(description)
                    xyz.note.ste_example = ste or ""
                    xyz.note.nonste_example = non_ste or ""
                case WordState.MEANING:
                    meanning = WordMeaning(
                        value=description or "",
                        ste_example=ste or "",
                        nonste_example=non_ste or "",
                    )
                    xyz.meanings.append(meanning)
                case WordState.MEANING_EXAMPLE:
                    meanning = WordMeaning(
                        value=description or "\u200b",
                        ste_example=ste or "",
                        nonste_example=non_ste or "",
                    )
                    xyz.meanings.append(meanning)
                case WordState.ALTERNATIVE:
                    assert description
                    alt_word = DictionaryInfo.get_single_word(description)
                    assert alt_word
                    alternative = Word(
                        status=alt_word.status,
                        name=alt_word.name,
                        type_=alt_word.type_,
                        source=WordSource.STE100_9,
                        meanings=[],
                        spellings=[],
                        alternatives=[],
                        ste_example=[],
                        nonste_example=[],
                    )
                    if ste:
                        alternative.ste_example.append(ste)
                    if non_ste:
                        alternative.nonste_example.append(non_ste)

                    xyz.alternatives.append(alternative)
                case WordState.ALTERNATIVE_EXAMPLE:
                    log.warning(
                        "[%s] ALTERNATIVE_EXAMPLE '%s (%s)': "
                        "alternative '%s' has multiple examples.",
                        item.filename,
                        item.word.name,
                        item.word.type_,
                        xyz.alternatives[-1].name,
                    )
                    if ste:
                        xyz.alternatives[-1].ste_example.append(ste)
                    if non_ste:
                        xyz.alternatives[-1].nonste_example.append(non_ste)
                case WordState.NOTE_ALTERNATIVE:
                    assert description
                    assert xyz.note
                    assert description
                    alt_word = DictionaryInfo.get_single_word(description)
                    assert alt_word
                    alternative = Word(
                        status=alt_word.status,
                        name=alt_word.name,
                        type_=alt_word.type_,
                        source=WordSource.STE100_9,
                        meanings=[],
                        spellings=[],
                        alternatives=[],
                        ste_example=[],
                        nonste_example=[],
                    )
                    if ste:
                        alternative.ste_example.append(ste)
                    if non_ste:
                        alternative.nonste_example.append(non_ste)
                    xyz.note.words.append(alternative)
                case WordState.NOTE_ALTERNATIVE_EXAMPLE:
                    assert xyz.note
                    log.warning(
                        "[%s] NOTE_ALTERNATIVE_EXAMPLE '%s (%s)': "
                        "alternative '%s' has multiple examples.",
                        item.filename,
                        item.word.name,
                        item.word.type_,
                        xyz.note.words[-1].name,
                    )
                case _:
                    raise ValueError(
                        f"[{previous_state}] --> [{current_state}] "
                        f"@ {line_info.get_type().name}: '{line_info}'"
                    )

        result = xyz
        return result

    def parse_source(
        self, path: Path, prefix: str, extension: str, dictionary_file_name: str
    ) -> None:
        """Parse OCR dictionary files."""

        assert path is not None and isinstance(path, Path)
        assert prefix is not None and "" != prefix
        assert extension is not None and "" != extension
        assert dictionary_file_name is not None and "" != dictionary_file_name

        log.debug("Parsing files in '%s' ...", path)

        files = [
            f
            for f in path.iterdir()
            if (f.is_file() and f.name.startswith(prefix) and f.suffix == extension)
        ]

        word_infos: list[WordInfo] = []
        for file in files:

            _, info = self.process_file(file)
            word_infos.extend(info)

        words: list[Word] = []
        for word_info in word_infos:

            word = self.process_wordinfo(word_info)
            if word is None:
                continue
            words.append(word)
            log.debug("word: [%s]", word)

        current_folder = Path(__file__).parent
        parsed_words_dicts = [asdict(entry) for entry in words]
        with open(
            file=(current_folder / dictionary_file_name),
            mode="w",
            encoding="utf-8",
            newline="\n",
        ) as f:
            json.dump(parsed_words_dicts, f, indent=2)

    def on_parse(self) -> None:
        """This is the handler for the `dictionary` command."""

        # How elegant!
        root_dir = Path(__file__).resolve().parent.parent.parent.parent.parent
        import_path = self._args.path
        path = root_dir.joinpath(import_path)
        prefix = self._args.prefix
        extension = self._args.extension
        dictionary_file_name = self._args.output
        self.parse_source(
            path=path,
            prefix=prefix,
            extension=extension,
            dictionary_file_name=dictionary_file_name,
        )
        return

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

        rule_theme = Theme(
            {
                # "markdown.h1": "bold magenta",
                # "markdown.h2": "bold cyan",
                "markdown.code": "red",
            }
        )
        console = Console(theme=rule_theme)

        current_folder = Path(__file__).parent
        rules_fullname = current_folder / self._rules_file_name
        rules = self._load_rules(rules_fullname)

        for rule in rules:

            if self._args.id:
                if not re.search(self._args.id, rule.id_, re.IGNORECASE):
                    continue

            if self._args.section:
                if not re.search(self._args.section, rule.section, re.IGNORECASE):
                    continue

            if self._args.category:
                if not re.search(self._args.category, rule.category, re.IGNORECASE):
                    continue

            p = Panel(
                f"[black]{rule.name}[/black]",
                title=f"Rule {rule.id_}",
                title_align="left",
                subtitle=f"{rule.section}, {rule.category}",
                subtitle_align="left",
                border_style="bright_black",
                style="on bright_yellow",
                padding=(1, 1),
                box=box.HEAVY_EDGE,
            )
            p = Panel(
                Markdown(rule.name),
                title=f"Rule {rule.id_}",
                title_align="left",
                subtitle=f"{rule.section}, {rule.category}, {rule.ref}",
                subtitle_align="left",
                border_style="bright_yellow",
                padding=(1, 1),
                box=box.HEAVY_EDGE,
            )
            console.print(p)
            md = Markdown(f"**{rule.summary}**")
            console.print("")
            console.print(md)
            console.print("")

            if self._args.summary:
                continue

            for content in rule.contents:
                match content.type_:
                    case RuleContentType.TEXT:
                        md = Markdown(content.data)
                        console.print(md)
                        console.print("")
                    case RuleContentType.EXAMPLE:
                        txt = f"[green]{content.data}[/green]"
                        console.print(
                            Panel(txt, title="STE", title_align="left", expand=False)
                        )
                        console.print("")
                    case RuleContentType.STE:
                        panel = MarkDownUtils.to_panel(
                            content.data, title="STE", style="green"
                        )
                        console.print(panel)
                        console.print("")
                    case RuleContentType.NONSTE:
                        panel = MarkDownUtils.to_panel(
                            content.data, title="Non-STE", style="red"
                        )
                        console.print(panel)
                        console.print("")
                    case RuleContentType.NOT_RECOMMENDED:
                        panel = MarkDownUtils.to_panel(
                            content.data, title="Not recommended", style="red"
                        )
                        console.print(panel)
                        console.print("")
                    case RuleContentType.NOTE:
                        md = Markdown(content.data)
                        console.print(
                            Panel(
                                md,
                                title="💡",
                                title_align="left",
                                border_style="yellow",
                                expand=False,
                            )
                        )
                        console.print("")
                    case RuleContentType.GOOD:
                        panel = MarkDownUtils.to_panel(
                            content.data, title="Example", style="green"
                        )
                        console.print(panel)
                        console.print("")
                    case RuleContentType.GENERAL:
                        panel = MarkDownUtils.to_panel(
                            content.data, title="Example", style="blue"
                        )
                        console.print(panel)
                        console.print("")
                    case RuleContentType.COMMENT:
                        md = Markdown(f"_{content.data}_")
                        console.print(md)
                        console.print("")
                    case _:
                        console.print("default")
                        md = Markdown(content.data)
                        console.print(md)
                        console.print("")
        return

    def on_dictionary(self) -> None:
        """This is the handler for the `dictionary` command."""

        dictionary_file_name = self._args.input

        assert dictionary_file_name is not None and "" != dictionary_file_name

        log.debug("Starting to parse source data ...")

        current_folder = Path(__file__).parent
        dictionary_fullname = current_folder / dictionary_file_name
        with open(dictionary_fullname, "r", encoding="utf-8") as f:
            dictionary_json = json.load(f)

        word_list = [
            from_dict(data_class=Word, data=item, config=self._dictionary_config)
            for item in dictionary_json
        ]
        dictionary = sorted(word_list, key=lambda e: e.name.lower())

        techncal_words = self._get_technical_words()
        dictionary.extend(techncal_words)

        dictionary = sorted(dictionary, key=lambda e: e.name.lower())

        self.prompt_user_loop(dictionary=dictionary)

        return

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

        if self._args.command == "dictionary":
            self.on_dictionary()
            return

        if self._args.command == "rules":
            self.on_rules()
            return

        if self._args.command == "parse":
            self.on_parse()
            return
