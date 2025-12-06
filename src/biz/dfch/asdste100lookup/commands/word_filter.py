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

"""WordFilter class."""

import re

from ..utils.enum_utils import enum_key_from_value
from ..word import Word
from ..word_category import WordCategory
from ..word_status import WordStatus
from ..word_type import WordType

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

        if (
            "" == self._filters[WordFilterType.TYPE]
            and "" == self._filters[WordFilterType.STATUS]
            and "" == self._filters[WordFilterType.SOURCE]
            and "" == self._filters[WordFilterType.CATEGORY]
            and "" == self._filters[WordFilterType.NOTE]
        ):
            return dictionary

        if "" != self._filters[WordFilterType.TYPE]:
            key = enum_key_from_value(
                WordType, self._filters[WordFilterType.TYPE]
            )
            type_ = WordType[key]

        if "" != self._filters[WordFilterType.STATUS]:
            key = enum_key_from_value(
                WordStatus, self._filters[WordFilterType.STATUS]
            )
            status = WordStatus[key]

        if "" != self._filters[WordFilterType.CATEGORY]:
            key = enum_key_from_value(
                WordCategory, self._filters[WordFilterType.CATEGORY]
            )
            category = WordCategory[key]

        if "" != self._filters[WordFilterType.SOURCE]:
            regex_source = re.compile(
                self._filters[WordFilterType.SOURCE], re.IGNORECASE
            )

        if "" != self._filters[WordFilterType.NOTE]:
            regex_note = re.compile(
                self._filters[WordFilterType.NOTE], re.IGNORECASE
            )

        result: list[Word] = []

        for word in dictionary:
            if "" != self._filters[WordFilterType.TYPE]:
                if word.type_ != type_:
                    continue

            if "" != self._filters[WordFilterType.STATUS]:
                if word.status != status:
                    continue

            if "" != self._filters[WordFilterType.CATEGORY]:
                if word.category != category:
                    continue

            if "" != self._filters[WordFilterType.SOURCE]:
                if not regex_source.search(word.source):
                    continue

            if "" != self._filters[WordFilterType.NOTE]:
                if not word.note or not regex_note.search(word.note.value):
                    continue

            result.append(word)

        return result
