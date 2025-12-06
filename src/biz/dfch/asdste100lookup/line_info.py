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

"""LineInfo class."""

from dataclasses import dataclass, field

from .column_index import ColumnIndex
from .dictionary_info import DictionaryInfo
from .line_info_type import LineInfoType


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

            # An value in the name column, that is not a word,
            # is an error.
            if not DictionaryInfo.is_word(name):
                return LineInfoType.ERROR

            # The first token is a word.
            # Possible types are:
            #   LineInfoType.WORD_MEANING
            #   LineInfoType.WORD_ALTERNATIVE
            #   LineInfoType.WORD_NOTE

            # A word in the name column, that has an empty description column,
            # is an error.
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
