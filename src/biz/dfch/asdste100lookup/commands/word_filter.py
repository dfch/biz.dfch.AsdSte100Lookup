# Copyright (c) 2025 - 2026 Ronald Rink, http://d-fens.ch
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

"""WordFilter class."""

import re

from biz.dfch.asdste100vocab import Word
from biz.dfch.asdste100vocab import WordCategory
from biz.dfch.asdste100vocab import WordStatus
from biz.dfch.asdste100vocab import WordType

from ..utils.enum_utils import enum_key_from_value

from .word_filter_type import WordFilterType


class WordFilter:  # pylint: disable=R0903
    """Implements the word filter for the dictionary."""

    _filters: dict

    def __init__(self, filters: dict):
        assert isinstance(filters, dict)

        self._filters = filters

    def invoke(self, dictionary: list[Word]) -> list[Word]:
        """
        Applies the current filter to `dictionary`
        and returns a new dictionary.
        """

        assert isinstance(dictionary, list)

        if self._no_filters_active():
            return dictionary

        resolved = self._resolve_filters()
        return [word for word in dictionary if self._matches_word(word, **resolved)]

    def _no_filters_active(self) -> bool:
        return all(
            "" == self._filters[f]
            for f in (
                WordFilterType.TYPE,
                WordFilterType.STATUS,
                WordFilterType.SOURCE,
                WordFilterType.CATEGORY,
                WordFilterType.NOTE,
            )
        )

    def _resolve_filters(self) -> dict:
        type_: WordType | None = None
        if "" != self._filters[WordFilterType.TYPE]:
            type_ = WordType[
                enum_key_from_value(WordType, self._filters[WordFilterType.TYPE])
            ]

        status: WordStatus | None = None
        if "" != self._filters[WordFilterType.STATUS]:
            status = WordStatus[
                enum_key_from_value(WordStatus, self._filters[WordFilterType.STATUS])
            ]

        category: WordCategory | None = None
        if "" != self._filters[WordFilterType.CATEGORY]:
            category = WordCategory[
                enum_key_from_value(
                    WordCategory, self._filters[WordFilterType.CATEGORY]
                )
            ]

        regex_source = None
        if "" != self._filters[WordFilterType.SOURCE]:
            regex_source = re.compile(
                self._filters[WordFilterType.SOURCE], re.IGNORECASE
            )

        regex_note = None
        if "" != self._filters[WordFilterType.NOTE]:
            regex_note = re.compile(self._filters[WordFilterType.NOTE], re.IGNORECASE)

        return {
            "type_": type_,
            "status": status,
            "category": category,
            "regex_source": regex_source,
            "regex_note": regex_note,
        }

    @staticmethod
    def _matches_word(
        word: Word,
        type_: WordType | None,
        status: WordStatus | None,
        category: WordCategory | None,
        regex_source,
        regex_note,
    ) -> bool:
        if type_ is not None and word.type_ != type_:
            return False
        if status is not None and word.status != status:
            return False
        if category is not None and word.category != category:
            return False
        if regex_source is not None and not regex_source.search(word.source):
            return False
        if regex_note is not None and (
            not word.note or not regex_note.search(word.note.value)
        ):
            return False
        return True
