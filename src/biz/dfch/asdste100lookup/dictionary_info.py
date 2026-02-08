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

"""DirectoryInfo class."""

from enum import StrEnum
import re
from typing import Type, TypeVar

from biz.dfch.asdste100vocab import WordStatus
from biz.dfch.asdste100vocab import WordType

from .dictionary_word import DictionaryWord
from .utils import get_value_or_default


T = TypeVar("T", bound=StrEnum)


def str_to_enum(enum_class: Type[T], value: str) -> T | None:
    """Convert a string to a StrEnum member, case-insensitively, by value."""
    # SONAR falsely complains, that enum_class is not iterable.
    for member in enum_class:  # NOSONAR
        if member.value.lower() == value.lower():
            return member

    raise ValueError(
        f"Invalid value: '{value}'.",
    )


class DictionaryInfo:
    """Provides utility functions for categorising text."""

    _pattern = re.compile(r"^([^\(]+) \((\w+)\),?")
    _pattern_single_word = re.compile(r"^([^\(]+) \((\w+)\)$")

    # Suppress sonar warning. If the user types in a too complex regex and the
    # programs cannot handle it, this is the fault of the user.
    _pattern_with_spellings = re.compile(
        r"""
        ^(\w+)               # 1. head word (e.g., WEAK)
        \s+\((\w+)\)         # 2. type in parentheses (e.g., adj)
        (?:\s+\(([^)]+)\))?  # 3. optional second parens (e.g., WEAKER, WEAKEST)
        (?:,\s*(.*))?        # 4. optional comma suffix (e.g., WALKS, WALKED, WALKED)  # noqa: disable:E501  # pylint: disable=C0301
        $
    """,
        re.VERBOSE,
    )  # NOSONAR

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
        return (get_value_or_default(value)).strip(DictionaryInfo.NOTE_MARKER)

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
