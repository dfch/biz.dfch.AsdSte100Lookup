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

from dataclasses import asdict, dataclass, field
from enum import auto, StrEnum, IntEnum, Enum
import json
from pathlib import Path
import re
from typing import Type, TypeVar
from rich.console import Console
from rich.table import Table

# from biz.dfch.i18n import LanguageCode
from biz.dfch.logging import log
from biz.dfch.version import Version

from .colouriser import Colouriser


class ColumnIndex(IntEnum):
    """Represent the column index in the source."""

    NAME = 0
    MEANING_ALT = 1
    STE = 2
    NONSTE = 3
    MAX_COLUMNS = 4


T = TypeVar("T", bound=StrEnum)


def str_to_enum(enum_class: Type[T], value: str) -> T | None:
    """Convert a string to a StrEnum member, case-insensitively, by value."""
    for member in enum_class:
        if member.value.lower() == value.lower():
            return member

    raise ValueError(
        f"Invalid value: '{value}'.",
    )


class WordType(StrEnum):
    """ASD-STE100 Issue 9 word types; cf. page 2-0-4f."""

    UNKNOWN = "unknown"
    NOUN = "n"
    VERB = "v"
    ADJECTIVE = "adj"
    ADVERB = "adv"
    PRONOUN = "pron"
    ARTICLE = "art"
    PREPOSITION = "prep"
    CONJUNCTION = "conj"
    PREFIX = "prefix"
    TECHNICAL_NAME = "TN"
    TECHNICAL_VERB = "TV"


class WordStatus(StrEnum):
    """Represents the status of a word."""

    UNKNOWN = "unknown"
    APPROVED = "approved"
    REJECTED = "rejected"


# @dataclass(frozen=True)
@dataclass
class WordNote:
    """Represents the ASD-STE100 note in the dictionary."""

    value: str
    # word: Word | None = None  # forward reference
    words: list[Word] = field(default_factory=list)  # forward reference
    ste_example: str | None = None
    nonste_example: str | None = None


@dataclass(frozen=True)
class WordMeaning:
    """Represents the ASD-STE100 defined meaning of a word."""

    value: str
    ste_example: str | None = None
    nonste_example: str | None = None
    note: WordNote | None = None


@dataclass(frozen=True)
class Word:
    """
    Represents either an approved or rejected word from the ASD-STE100 standard.
    """

    status: WordStatus
    name: str
    type_: WordType
    meanings: list[WordMeaning]
    spellings: list[str]
    alternatives: list[Word]
    ste_example: str | None = None
    nonste_example: str | None = None
    note: WordNote | None = None


@dataclass
class TableRow:
    """Represents a single row in the table."""

    word: str | None = None
    description: str | None = None
    ste_example: str | None = None
    nonste_example: str | None = None


@dataclass
class LineInfo:
    """Contains information about a line in the dictionary."""

    is_start_of_word: bool = False
    line: str = ""
    tokens: list[str] = field(default_factory=list)
    tokens_count: int = 0
    is_processed: bool = False

    def _get_token(self, index: ColumnIndex) -> str | None:

        if len(self.tokens) <= index:
            return None

        result = self.tokens[index].strip()
        return result or None

    def get_type(self) -> LineInfoType:
        """Returns the LineInfoType of the specified LineInfo."""

        if self.tokens_count <= ColumnIndex.NAME:
            return LineInfoType.ERROR

        name = self.get_name()
        description = self.get_description()
        ste = self.get_ste()
        nonste = self.get_nonste()

        # The first token is not empty.
        # Possible types are:
        #   LineInfoType.WORD_MEANING
        #   LineInfoType.WORD_ALTERNATIVE
        #   LineInfoType.WORD_NOTE
        if name:

            # A note in the name column is an error.
            if name.startswith(DictionaryInfo.NOTE_MARKER):
                return LineInfoType.ERROR

            # An value in the name column, that is not a word, is an error.
            if not DictionaryInfo.is_word(name):
                return LineInfoType.ERROR

            # The first token is a word.
            # Possible types are:
            #   LineInfoType.WORD_MEANING
            #   LineInfoType.WORD_ALTERNATIVE
            #   LineInfoType.WORD_NOTE

            # A word in the name column, that has an empty description column, is an error.
            if not description:
                return LineInfoType.ERROR

            # The first token is a word.
            # The second token is not empty.
            # The second token is a note.
            # Possible types are:
            #   LineInfoType.WORD_NOTE
            if description.startswith(DictionaryInfo.NOTE_MARKER):
                return LineInfoType.NOTE

            # The first token is a word.
            # The second token is not empty.
            # The second token is a word.
            # Possible types are:
            #   LineInfoType.WORD_ALTERNATIVE
            if DictionaryInfo.is_single_word(description):
                return LineInfoType.ALTERNATIVE

            # The first token is a word.
            # The second token is not empty.
            # The second token is not a word.
            # Possible types are:
            #   LineInfoType.WORD_MEANING
            return LineInfoType.MEANING

        # The first token is empty.
        # Possible types are:
        #   LineInfoType.WORD_MEANING
        #   LineInfoType.WORD_ALTERNATIVE
        #   LineInfoType.WORD_NOTE
        #   LineInfoType.EXAMPLE

        # The first token is empty.
        # The second token is not empty.
        # Possible types are:
        #   LineInfoType.WORD_MEANING
        #   LineInfoType.WORD_ALTERNATIVE
        #   LineInfoType.WORD_NOTE
        if description:

            # The first token is empty.
            # The second token is not empty.
            # The second token is a note.
            # Possible types are:
            #   LineInfoType.WORD_NOTE
            if description.startswith(DictionaryInfo.NOTE_MARKER):
                return LineInfoType.NOTE

            # The first token is empty.
            # The second token is not empty.
            # The second token is a word.
            # Possible types are:
            #   LineInfoType.WORD_ALTERNATIVE
            if DictionaryInfo.is_single_word(description):
                return LineInfoType.ALTERNATIVE

            # The first token is empty.
            # The second token is not empty.
            # The second token is a not word.
            # Possible types are:
            #   LineInfoType.WORD_MEANING
            return LineInfoType.MEANING

        # The first token is empty.
        # The second token is empty.
        # Possible types are:
        #   LineInfoType.EXAMPLE

        # The first token is empty.
        # The second token is empty.
        # The third token is not empty.
        # Possible types are:
        #   LineInfoType.EXAMPLE
        if ste:
            return LineInfoType.EXAMPLE

        # The first token is empty.
        # The second token is empty.
        # The third token is empty.
        # The fourth token is not empty.
        # Possible types are:
        #   LineInfoType.EXAMPLE
        if nonste:
            return LineInfoType.EXAMPLE

        # An empty value in all four columns is an error.
        return LineInfoType.ERROR

    def get_name(self) -> str | None:
        """Returns the name part or None of LineInfo."""
        return self._get_token(ColumnIndex.NAME)

    def get_description(self) -> str | None:
        """Returns the meaning or alt part or None of LineInfo."""
        return self._get_token(ColumnIndex.MEANING_ALT)

    def get_ste(self) -> str | None:
        """Returns the ste_example part or None of LineInfo."""
        return self._get_token(ColumnIndex.STE)

    def get_nonste(self) -> str | None:
        """Returns the nonste_example part or None of LineInfo."""
        return self._get_token(ColumnIndex.NONSTE)


@dataclass
class DictionaryWord:
    """Represents a word from the dictionary."""

    name: str = ""
    type_: WordType = WordType.UNKNOWN
    status: WordStatus = WordStatus.UNKNOWN


@dataclass
class WordInfo:
    """Contains information about a word in the dictionary."""

    filename: str
    word: DictionaryWord = field(default_factory=DictionaryWord)
    line_infos: list[LineInfo] = field(default_factory=list)


class WordState(Enum):
    """Represents the state of a Word."""

    INITIAL = auto()
    ERROR = auto()

    WORD_MEANING = auto()
    WORD_ALTERNATIVE = auto()
    WORD_NOTE = auto()

    ALTERNATIVE = auto()
    ALTERNATIVE_EXAMPLE = auto()

    MEANING = auto()
    MEANING_EXAMPLE = auto()

    NOTE = auto()
    NOTE_ALTERNATIVE = auto()
    NOTE_ALTERNATIVE_EXAMPLE = auto()


class LineInfoType(Enum):
    """Represents the type of a LineInfo"""

    ERROR = auto()
    MEANING = auto()
    ALTERNATIVE = auto()
    NOTE = auto()
    EXAMPLE = auto()


class DictionaryInfo:
    """Provides utility functions for categorising text."""

    # _pattern = re.compile(r"[^\(]+ \(\w+\)")
    _pattern = re.compile(r"^([^\(]+) \((\w+)\),?")
    _pattern_single_word = re.compile(r"^([^\(]+) \((\w+)\)$")

    _pattern_with_spellings = re.compile(
        r"""
        ^(\w+)               # 1. head word (e.g., WEAK)
        \s+\((\w+)\)         # 2. type in parentheses (e.g., adj)
        (?:\s+\(([^)]+)\))?  # 3. optional second parens (e.g., WEAKER, WEAKEST)
        (?:,\s*(.*))?        # 4. optional comma suffix (e.g., WALKS, WALKED, WALKED)
        $
    """,
        re.VERBOSE,
    )

    NOTE_MARKER: str = "###"

    @staticmethod
    def is_word(value: str | None) -> bool:
        """Determines whether a given string contains an approved word."""

        result: bool = False

        if value is None or "" == value:
            return result

        if DictionaryInfo._pattern.match(value):
            result = True

        return result

    @staticmethod
    def is_single_word(value: str | None) -> bool:
        """Determines whether a given string is a word."""

        result: bool = False

        if value is None or "" == value:
            return result

        if DictionaryInfo._pattern_single_word.match(value):
            result = True

        return result

    @staticmethod
    def get_word(value: str | None) -> DictionaryWord | None:
        """Extracts the word information from a valid word."""

        if value is None or "" == value:
            return None

        result: DictionaryWord = DictionaryWord()

        match = DictionaryInfo._pattern.match(value)
        if not match:
            return None

        result.name = match.group(1).strip()
        type_ = str_to_enum(WordType, match.group(2))
        assert type_ is not None
        result.type_ = type_

        if result.name.isupper():
            result.status = WordStatus.APPROVED
        elif result.name.islower():
            result.status = WordStatus.REJECTED
        else:
            result.status = WordStatus.UNKNOWN

        return result

    @staticmethod
    def get_single_word(value: str | None) -> DictionaryWord | None:
        """Extracts the word information from a single word."""

        if value is None or "" == value:
            return None

        result: DictionaryWord = DictionaryWord()

        match = DictionaryInfo._pattern_single_word.fullmatch(value.strip())
        if not match:
            return None

        result.name = match.group(1).strip()
        type_ = str_to_enum(WordType, match.group(2))
        assert type_ is not None
        result.type_ = type_

        if result.name.isupper():
            result.status = WordStatus.APPROVED
        elif result.name.islower():
            result.status = WordStatus.REJECTED
        else:
            result.status = WordStatus.UNKNOWN

        return result

    @staticmethod
    def get_note(value: str | None) -> str:
        """Extracts the note from a string."""
        return (value or "").strip(DictionaryInfo.NOTE_MARKER)

    @staticmethod
    def get_spellings(value: str | None) -> list[str]:
        """Extracts the spellings from a string."""

        result: list[str] = []

        if value is None or "" == value:
            return result

        match = DictionaryInfo._pattern_with_spellings.match(value)
        if not match:
            return result

        word_name = match.group(1)
        assert word_name is not None and "" != word_name
        word_type = match.group(2)
        assert word_type is not None and "" != word_type

        spellings_conjugated = match.group(3)  # from (WEAKER, WEAKEST)
        spellings_declinated = match.group(4)  # from ", WALKS, WALKED, WALKED"

        if spellings_conjugated:
            result += [w.strip() for w in spellings_conjugated.split(",")]
        if spellings_declinated:
            result += [w.strip() for w in spellings_declinated.split(",")]

        return result


class App:  # pylint: disable=R0903
    """The application."""

    _VERSION_REQUIRED_MAJOR = 3
    _VERSION_REQUIRED_MINOR = 11

    # Note: also adjust in pyproject.toml
    _VERSION = "1.0.1-beta"
    _PROG_NAME = "scnfmixr"

    def __init__(self):

        Version().ensure_minimum_version(
            self._VERSION_REQUIRED_MAJOR, self._VERSION_REQUIRED_MINOR
        )

    def to_colour(self, text: str, value: str, status: str) -> str:
        """Colourises value in specified text green or red based on status."""
        if WordStatus.APPROVED == status:
            result = Colouriser(text).to_green(value)
        else:
            result = Colouriser(text).to_red(value)

        return result

    def prompt_user_loop(self) -> None:
        """Main program loop."""

        log.debug("Starting to parse source data ...")

        print(
            f"AsdSte100Lookup (A dictionary lookup tool for ASD-STE100), v{self._VERSION}\n"
            "Copyright 2025 Ronald Rink. Licensed under GPLv3.\n"
            "ASD-STE100 Simplified Technical English "
            "(Standard for Technical Documentation) Issue 9.\n"
            "Copyright 2025 European Aerospace, Security and Defence Industry"
            ", https://www.asd-europe.org.",
        )

        dictionary_fullname = Path(__file__).parent / "dictionary.json"
        with open(dictionary_fullname, "r", encoding="utf-8") as f:
            dictionary_json = json.load(f)

        assert isinstance(dictionary_json, list)
        for word in dictionary_json:
            assert isinstance(word, dict)

        dictionary = [Word(**entry) for entry in dictionary_json]
        dictionary = sorted(
            [Word(**entry) for entry in dictionary_json], key=lambda e: e.name.lower()
        )

        console = Console()
        while True:
            prompt = input(f"[{len(dictionary)}] Enter search term: ").strip()
            if prompt is None or "" == prompt:
                log.debug("Exiting ...")
                break

            # Create the table
            # table = Table(title=f"Results: '{prompt}'")
            table = Table()
            table.add_column("Word", no_wrap=True, min_width=16)
            table.add_column("Meaning/ALTERNATIVE", min_width=16)
            table.add_column("STE Example")
            table.add_column("Non-STE Example")

            matching_words = {}
            try:
                for word in dictionary:
                    if re.search(prompt, word.name, re.IGNORECASE):
                        matching_words[id(word)] = word
                        continue

                    for spelling in word.spellings:
                        if re.search(prompt, spelling, re.IGNORECASE):
                            matching_words[id(word)] = word
                            continue

                    if word.ste_example and re.search(
                        prompt, word.ste_example, re.IGNORECASE
                    ):
                        matching_words[id(word)] = word
                        continue

                    if word.nonste_example and re.search(
                        prompt, word.nonste_example, re.IGNORECASE
                    ):
                        matching_words[id(word)] = word
                        continue
            except re.error as ex:
                log.error("Invalid regex: '%s'", ex)

            rows: list[TableRow] = []
            for word in matching_words.values():

                row = TableRow()
                rows.append(row)
                is_approved = WordStatus.APPROVED == word.status

                if is_approved:
                    if word.name:
                        row.word = self.to_colour(
                            f"{word.name.upper()} ({word.type_})",
                            word.name,
                            word.status,
                        )
                    if word.ste_example:
                        row.ste_example = self.to_colour(
                            word.ste_example, prompt, word.status
                        )
                else:
                    if word.name:
                        row.word = self.to_colour(
                            f"{word.name.lower()} ({word.type_})",
                            word.name,
                            word.status,
                        )
                    if word.nonste_example:
                        row.nonste_example = self.to_colour(
                            word.nonste_example, prompt, WordStatus.REJECTED
                        )

                if word.spellings:
                    colourised_spellings: list[str] = [
                        str(Colouriser(x, "blue")) for x in word.spellings
                    ]

                    spellings = "\n".join(colourised_spellings)
                    row.word = f"{row.word}\n{spellings}"

                if word.meanings:
                    meanings = [WordMeaning(**entry) for entry in word.meanings]
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
                    alternatives = [Word(**entry) for entry in word.alternatives]
                    for alt in alternatives:
                        if row.description:
                            row = TableRow()
                            rows.append(row)

                        row.description = self.to_colour(
                            f"{alt.name.upper()} ({alt.type_})", alt.name, alt.status
                        )
                        if alt.ste_example:
                            row.ste_example = self.to_colour(
                                alt.ste_example, alt.name, alt.status
                            )
                        if alt.nonste_example:
                            row.nonste_example = self.to_colour(
                                alt.nonste_example, word.name, WordStatus.REJECTED
                            )

                if word.note:
                    if isinstance(word.note, WordNote):
                        note = word.note
                    else:
                        note = WordNote(**word.note)

                    if note.words:
                        nwords = [Word(**entry) for entry in note.words]

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
                            if nword.ste_example:
                                row.ste_example = self.to_colour(
                                    nword.ste_example, nword.name, WordStatus.APPROVED
                                )
                            if nword.nonste_example:
                                row.nonste_example = self.to_colour(
                                    nword.nonste_example, word.name, WordStatus.REJECTED
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
                    # log.debug(f"'{row.word}', '{row.description}', '{row.ste_example}', '{row.nonste_example}'")
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

    def extract_simple_note(self, line_info: LineInfo) -> WordNote | None:
        """Extracts a simple one-liner WordNote from LineInfo."""

        assert line_info is not None

        tokens = line_info.tokens

        if line_info.tokens_count <= ColumnIndex.MEANING_ALT:
            return None

        meaning_or_alt = tokens[ColumnIndex.MEANING_ALT].strip()
        if not meaning_or_alt.startswith(DictionaryInfo.NOTE_MARKER):
            return None

        meaning_or_alt = meaning_or_alt.strip(DictionaryInfo.NOTE_MARKER)
        result = WordNote(meaning_or_alt)

        ste_example = ""
        if line_info.tokens_count > ColumnIndex.STE:
            ste_example = tokens[ColumnIndex.STE]
            result.ste_example = ste_example

        nonste_example = ""
        if line_info.tokens_count > ColumnIndex.NONSTE:
            nonste_example = tokens[ColumnIndex.NONSTE]
            result.nonste_example = nonste_example

        return (
            result
            if any(
                s in meaning_or_alt
                for s in [
                    DictionaryInfo.IF_MORE_ACCURATE_CORRECT,
                    DictionaryInfo.IF_MORE_ACCURATE,
                    DictionaryInfo.IF_MORE_ACCURATE_VERB,
                    DictionaryInfo.FREQUENTLY_NO_ALTERNATIVE,
                    DictionaryInfo.AS_LONG_AS,
                    DictionaryInfo.IF_MORE_CLEAR_AND_ACCURATE,
                    DictionaryInfo.IF_MORE_CLEAR_AND_ACCURATE,
                    DictionaryInfo.NO_OTHER_VERB_FORM,
                    DictionaryInfo.DO_NOT_USE_COULD,
                    DictionaryInfo.ALSO_USE_DIFFERENT,
                    DictionaryInfo.USE_IF,
                    DictionaryInfo.DANGER_SECTION_7,
                    DictionaryInfo.USE_SINGULAR,
                ]
            )
            else None
        )

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
            meanings=[],
            spellings=[],
            alternatives=[],
            ste_example=ste_example,
            nonste_example=nonste_example,
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
            f"[{item.filename}] [{current_state.name} --> {next_state.name}] @ {line_info.get_type().name}: {line_info.line}"
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
                    type_=item.word.type_,
                    name=item.word.name,
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
                    meanings=[],
                    spellings=[],
                    alternatives=[],
                    ste_example=ste or "",
                    nonste_example=non_ste or "",
                )
                xyz = Word(
                    status=item.word.status,
                    type_=item.word.type_,
                    name=item.word.name,
                    meanings=[],
                    spellings=spellings,
                    alternatives=[alternative],
                    note=WordNote(value=""),
                )
            case WordState.WORD_NOTE:
                xyz = Word(
                    status=item.word.status,
                    type_=item.word.type_,
                    name=item.word.name,
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
                        meanings=[],
                        spellings=[],
                        alternatives=[],
                        ste_example=ste or "",
                        nonste_example=non_ste or "",
                    )
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
                        meanings=[],
                        spellings=[],
                        alternatives=[],
                        ste_example=ste or "",
                        nonste_example=non_ste or "",
                    )
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
        self,
        path: Path,
        prefix: str = "ASD-STE100 - ",
        extension: str = ".txt",
    ) -> None:
        """Parse OCR dictionary files."""

        assert path is not None and isinstance(path, Path)
        assert prefix is not None and "" != prefix
        assert extension is not None and "" != extension

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

        parsed_words_dicts = [asdict(entry) for entry in words]
        with open(
            file="./biz/dfch/asdste100lookup/dictionary.json",
            mode="w",
            encoding="utf-8",
            newline="\n",
        ) as f:
            json.dump(parsed_words_dicts, f, indent=2)

    def invoke(self) -> None:
        """Main entry point for this class."""

        log.debug("Invoke.")

        # Elegant!
        root_dir = Path(__file__).resolve().parent.parent.parent.parent.parent
        path = root_dir.joinpath("ASD-STE100/v3/txt")
        self.parse_source(path=path)
        self.prompt_user_loop()
